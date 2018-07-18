from django.shortcuts import render_to_response,redirect,render,get_object_or_404
from django.template.loader import render_to_string
from .models import Config,Seq,Shift
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import SKUForm,EditForm,DeleteForm,OrderForm,ShiftForm,StnForm
from django.http import JsonResponse
from django.db.models import Sum,Max,Count,Min
from gen import main,sub
from numpy import sum

@csrf_exempt
def Configuration(request):
 if request.method == 'POST':
  form=SKUForm(request.POST)
  if form.is_valid():
   Obj=form.cleaned_data
   model=Obj['model']
   variant=Obj['variant']
   color=Obj['color']
   time=Obj['time']
   if not (Config.objects.filter(model=model,variant=variant,color=color).exists()):
    form.save()
    form=form.save()
    data='New SKU added. Go to Line Monitoring to configure station TAKT times.'
   else:
    data='This configuration already exists.'
    form=SKUForm()
    view=Config.objects.all().values()
    return render_to_response('app/configuration.html',{'form':form,'data':data,'view':view,},RequestContext(request))
  else:
   data='Invalid Configuration'
 form=SKUForm()
 data=''
 view=Config.objects.all().values()
 return render_to_response('app/configuration.html',{'form':form,'data':data,'view':view,},RequestContext(request))

@csrf_exempt
def Edit(request):
 data=dict()
 if request.method == 'POST':
  form=Edit(request.POST)
  if form.is_valid():
   data['form_is_valid'] = True
   Obj=form.cleaned_data
   SKU=Obj['SKU']
   model=Obj['model']
   variant=Obj['variant']
   color=Obj['color']
   tank=Obj['tank']
   time=Obj['time']
   description=Obj['description']
   if not (Config.objects.filter(model=model,variant=variant,color=color).exists()):
    Config.objects.filter(SKU=SKU).update(model=model,variant=variant,color=color,tank=tank,time=time,description=description)
   view=Config.objects.all().values()
   data['sku_list']=render_to_string('app/partial_list.html', {'view': view})
  else:
   data['form_is_valid'] = False
 else:
  form=EditForm()
  context={'form': form}
  data['html_form']=render_to_string('app/edit_popup.html',context,request=request)
 return JsonResponse(data)

@csrf_exempt
def Delete(request):
 data=dict()
 if request.method == 'POST':
  form=Delete(request.POST)
  if form.is_valid():
   data['form_is_valid'] = True
   Obj=form.cleaned_data
   SKU=Obj['SKU']
   Config.objects.filter(SKU=SKU).delete()
   view = Config.objects.all().values()
   data['sku_list'] = render_to_string('app/partial_list.html', {'view': view})
  else:
   data['form_is_valid'] = False
 else:
  form = DeleteForm()
  context = {'form': form}
  data['html_form'] = render_to_string('app/delete_popup.html',context,request=request)
 return JsonResponse(data)

@csrf_exempt
def Production(request):
 if 'config' in request.POST:
  form = OrderForm(request.POST)
  if form.is_valid():
   Obj = form.cleaned_data
   SKU = Obj['SKU']
   quantity = Obj['quantity']
   skips = Obj['skips']
   strips = Obj['strips']
   if (bool(Obj.get('ratio', False))):
    ratio = Obj['ratio']
   else:
    ratio = Obj['quantity']
   Config.objects.filter(SKU=SKU).update(quantity=quantity,ratio=ratio,skips=skips,strips=strips)
  else:
   data='Invalid Order.'
 elif 'shift' in request.POST:
  forms = ShiftForm(request.POST)
  if forms.is_valid():
   Obj = forms.cleaned_data
   A = Obj['A']
   B = Obj['B']
   C = Obj['C']
   Shift.objects.filter(name='Shift').update(A=A,B=B,C=C)
  else:
   data='Invalid Shift Timings.'
 form = OrderForm()
 forms = ShiftForm()
 data =''
 view = Config.objects.all().values()
 return render_to_response( 'app/production.html',{'form':form,'forms':forms,'data':data,'view':view}, RequestContext(request))

def Validate(request):
 data=dict()
 Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
 Total_Shift_Time=list(Shift.objects.filter(name='Shift').values_list('A','B','C'))
 Total_Shift_Time=sum(Total_Shift_Time)
 Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
 Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
 if(Total_Order>Capacity):
  data['Output'] = 'Capacity is being exceeded, Reduce orders!'
 else:
  data['Output'] = 'Orders are within capacity, Sequence can now be generated!'
 return JsonResponse(data)

def Sequence(request):
 tq=[]
 Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
 Ratio_Sum=list(Config.objects.aggregate(Sum('ratio')).values())[0]
 Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
 SKU_Count=list(Config.objects.aggregate(Count('SKU')).values())[0]
 if Config.objects.filter(SKU__range=(0,SKU_Count),quantity=0).exists():
  SKU_Count=SKU_Count-1
 Seq_Q=Seq.objects.all().count()
 tl = Config.objects.values_list('stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')
 forsub = Config.objects.exclude(quantity=0).values_list('SKU','quantity','ratio','skips','strips')
 for key in forsub:
  tq.append(key[1])
 Div = list(Config.objects.aggregate(Min('quantity')).values())[0]
 Total_Shift_Time=list(Shift.objects.filter(name='Shift').values_list('A','B','C'))
 Total_Shift_Time=sum(Total_Shift_Time)
 Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
 if(Total_Order<Capacity):
  Sequenced=[]
  P2_Obj=[]
  P2_Seq=[]
  P2_Config=[]
  Seq.objects.filter(Sq_No__range=(Total_Order+1,Seq_Q)).delete()
  sku_ratio = Config.objects.filter(SKU__range=(0,SKU_Count)).values_list('SKU','ratio')
  for x in range(0,Total_Order//Ratio_Sum):
   for key,value in sku_ratio:
    for value in range(value):
     Sequenced.append(key)
  time = main(Sequenced,tq,tl)
  data = 'Time Taken: ' +str(time//60)+ ' minutes'
  for value in Sequenced:
   P2_Obj.append(Config.objects.get(SKU=value))
   P2_Config.append(Config.objects.filter(SKU=value).values('SKU','model','variant','color','tank'))
  for x in range(0,Total_Order):
   if not (Seq.objects.filter(Sq_No=x+1).exists()):
    Seq.objects.create(Sq_No=x+1,SKU=P2_Obj[x])
   else:
    Seq.objects.filter(Sq_No=x+1).update(SKU=P2_Obj[x])
   P2_Seq.append(Seq.objects.filter(Sq_No=x+1).values('Sq_No','status'))
  Sequence = list(zip(P2_Seq, P2_Config))
 else: #Check
  data='Capacity is being exceeded, Reduce orders!'
 return render_to_response( 'app/sequence.html',{'Sequence':Sequence,'data':data}, RequestContext(request))

def Optimize(request):
  tq=[]
  P3_Seq=[]
  P3_Config=[]
  P3_Obj=[]
  Color_Blocked=[]
  Ratio_val_color=[]
  tSeq=[]
  Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
  Ratio_Sum=list(Config.objects.aggregate(Sum('ratio')).values())[0]
  forsub = Config.objects.exclude(quantity=0).values_list('SKU','quantity','ratio','skips','strips').order_by('color')
  tl = Station.objects.values_list('stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')
  for key in forsub:
   tq.append(key[1])
   Color_Blocked.append(key[0])
  for i in Color_Blocked:
   Ratio_val_color.append(Config.objects.filter(SKU=i).values('ratio')[0]['ratio'])
  Color_Blocked = list(zip(Color_Blocked, Ratio_val_color))
  for x in range (0,Total_Order//Ratio_Sum):
   for key,value in Color_Blocked:
    for value in range(value):
     tSeq.append(key)
  time = main(tSeq,tq,tl)
  data = 'Time Taken: ' +str(time//60)+ ' minutes'
  for value in tSeq:
   P3_Obj.append(Config.objects.get(SKU=value))
   P3_Config.append(Config.objects.filter(SKU=value).values('SKU','model','variant','color','tank'))
  for x in range(0,Total_Order):
   Seq.objects.filter(Sq_No=x+1).update(SKU=P3_Obj[x])
   P3_Seq.append(Seq.objects.filter(Sq_No=x+1).values('Sq_No','status'))
  Sequence = list(zip(P3_Seq,P3_Config))
  return render_to_response( 'app/sequence.html',{'Sequence':Sequence,'data':data}, RequestContext(request))


def Start(request):
 Sq_No = request.GET.get('Sq_No', None)
 Seq.objects.filter(Sq_No=Sq_No).update(status='Running')
 view =  Seq.objects.filter(SKU_id=sku).values('status')
 context = {'view': view}
 data['html_form'] = render_to_string('app/partial_list.html',context,request=request)
 return JsonResponse(data)

@csrf_exempt
def Line(request):
 if request.method == 'POST':
  form = StnForm(request.POST)
  if form.is_valid():
   Obj = form.cleaned_data
   SKU = Obj['SKU']
   if (Config.objects.filter(SKU=SKU).exists()):
    stn1 = Obj['stn1']
    stn2 = Obj['stn2']
    stn3 = Obj['stn3']
    stn4 = Obj['stn4']
    stn5 = Obj['stn5']
    stn6 = Obj['stn6']
    stn7 = Obj['stn7']
    stn8 = Obj['stn8']
    stn9 = Obj['stn9']
    stn10 = Obj['stn10']
    Config.objects.filter(SKU=SKU).update(stn1=stn1,stn2=stn2,stn3=stn3,stn4=stn4,stn5=stn5,stn6=stn6,stn7=stn7,stn8=stn8,stn9=stn9,stn10=stn10)
   else:
    data = 'SKU does not exist.'
    form = StnForm()
    return render_to_response('app/line.html',{'form':form,'data':data}, RequestContext(request))
  else:
   data = 'Cannot Add,Invalid Station Timings'
 data=''
 form = StnForm()
 return render_to_response('app/line.html',{'form':form,'data':data}, RequestContext(request))

def Populate(request):
 data=dict()
 stn=[]
 SKU = request.GET.get('sku', None)
 if (Config.objects.filter(SKU=SKU).exists()):
  stn = Config.objects.filter(SKU=SKU).values_list('stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')[0]
  for key in stn:
   data = {
   'stn1' : stn[0],
   'stn2' : stn[1],
   'stn3' : stn[2],
   'stn4' : stn[3],
   'stn5' : stn[4],
   'stn6' : stn[5],
   'stn7' : stn[6],
   'stn8' : stn[7],
   'stn9' : stn[8],
   'stn10' : stn[9],
   'Output' : 'Success!'
   }
 else:
  data['Output'] = 'SKU does not exist.'
 return JsonResponse(data)
