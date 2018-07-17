from django.shortcuts import render_to_response,redirect,render,get_object_or_404
from django.template.loader import render_to_string
from .models import Constraint,Config,Seq,Station,Shift
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import SKUDef,EditForm,DeleteForm,OrderForm,ConstraintForm,ShiftForm,StnForm
from django.http import JsonResponse
from django.db.models import Sum,Max,Count,Min
from gen import main,sub
from numpy import sum

@csrf_exempt
def Configuration(request):
 data=dict()
 if request.method == 'POST':
  form=SKUDef(request.POST)
  if form.is_valid():
   Obj=form.cleaned_data
   model=Obj['model']
   variant=Obj['variant']
   color=Obj['color']
   if (Config.objects.filter(model=model,variant=variant,color=color).exists()):
    data='This configuration already exists.'
   else:
    form=form.save()
    form.save()
  else:
   data='Invalid Form'
 form=SKUDef()
 view=Config.objects.all().values()
 return render_to_response('app/configuration.html',{'form':form,'view':view,'data':data},RequestContext(request))

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
 data = dict()
 if request.method == 'POST':
  form = Delete(request.POST)
  if form.is_valid():
   data['form_is_valid'] = True
   Obj = form.cleaned_data
   SKU = Obj['SKU']
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
   print('Config Error')
 elif 'shift' in request.POST:
  forms = ShiftForm(request.POST)
  if forms.is_valid():
   Obj = forms.cleaned_data
   A = Obj['A']
   B = Obj['B']
   C = Obj['C']
   Shift.objects.filter(name='Shift').update_or_create(A=A,B=B,C=C)
 elif 'constraint' in request.POST:
  formed = ConstraintForm(request.POST)
  if formed.is_valid():
   Obj = formed.cleaned_data
   Color_Blocked = Obj['Color_Blocked']
   Constraint.objects.filter(name='Constraint').update_or_create(Color_Blocked=Color_Blocked)
  else:
   print('Constraint Error')
 form = OrderForm()
 forms = ShiftForm()
 formed = ConstraintForm()
 view = Config.objects.all().values()
 return render_to_response( 'app/production.html',{'form':form,'view':view,'forms':forms,'formed':formed}, RequestContext(request))

def Validate(request):
 data = dict()
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
 Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
 Ratio_Sum=list(Config.objects.aggregate(Sum('ratio')).values())[0]
 Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
 SKU_Count=list(Config.objects.aggregate(Count('SKU')).values())[0]
 if Config.objects.filter(SKU__range=(0,SKU_Count),quantity=0).exists():
  SKU_Count=SKU_Count-1
 Seq_Q=Seq.objects.all().count()
 tl = Station.objects.values_list('stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')
 t = Config.objects.exclude(quantity=0)
 forsub = t.values_list('SKU','quantity','ratio','skips','strips')
 tq = t.values_list('quantity',flat=True)
 Sequence = sub(forsub,Total_Order)
 Div = list(Config.objects.aggregate(Min('quantity')).values())[0]
 Total_Shift_Time=list(Shift.objects.filter(name='Shift').values_list('A','B','C'))
 Total_Shift_Time=sum(Total_Shift_Time)
 Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
 if(Total_Order<Capacity):
  #List for Phase2
  Sequenced=[]
  P2_Obj=[]
  P2_Seq=[]
  P2_Config=[]
  Sequence1=[]
  #List for Color Blocking
  P3_Seq=[]
  P3_Config=[]
  P3_Obj=[]
  SKU_val_color=[]
  Ratio_val_color=[]
  tSeq=[]
  Sequence2=[]
  Seq.objects.filter(Sq_No__range=(Total_Order+1,Seq_Q)).delete()
  #Phase2
  sku_ratio = Config.objects.filter(SKU__range=(0,SKU_Count)).values_list('SKU','ratio')
  for x in range(0,Total_Order//Ratio_Sum):
   for key,value in sku_ratio:
    for value in range(value):
     Sequenced.append(key)
  for value in Sequenced:
   P2_Obj.append(Config.objects.get(SKU=value))
  for x in range(0,Total_Order):
   if not (Seq.objects.filter(Sq_No=x+1).exists()):
    Seq.objects.create(Sq_No=x+1,SKU=P2_Obj[x])
   else:
    Seq.objects.filter(Sq_No=x+1).update(SKU=P2_Obj[x])
   P2_Seq.append(Seq.objects.filter(Sq_No=x+1).values())
   P2_Config.append(Config.objects.filter(SKU=Seq.objects.filter(Sq_No=x+1).values('SKU_id')[0]['SKU_id']).values())
   Sequence1 = list(zip(P2_Seq, P2_Config))
  #Color Blocking
  Color_Blocked=Config.objects.exclude(quantity=0,ratio=0).values('SKU').order_by('color')
  for key in Color_Blocked:
   SKU_val_color.append(key['SKU'])
  for i in SKU_val_color:
   Ratio_val_color.append(Config.objects.filter(SKU=i).values('ratio')[0]['ratio'])
  Color_Blocked = list(zip(SKU_val_color, Ratio_val_color))
  for x in range (0,Total_Order//Ratio_Sum):
   for key,value in Color_Blocked:
    for value in range(value):
     tSeq.append(key)
  time = main(tSeq,tq,tl)
  data = 'Time Taken: ' + str(time) + ' seconds'
  for value in tSeq:
   P3_Obj.append(Config.objects.get(SKU=value))
  for x in range(0,Total_Order):
   Seq.objects.filter(Sq_No=x+1).update(SKU=P3_Obj[x])
   P3_Seq.append(Seq.objects.filter(Sq_No=x+1).values())
   P3_Config.append(Config.objects.filter(SKU=Seq.objects.filter(Sq_No=x+1).values('SKU_id')[0]['SKU_id']).values())
   Sequence2 = list(zip(P3_Seq,P3_Config))
 return render_to_response( 'app/sequence.html',{'Sequence1':Sequence1,'Sequence2':Sequence2,'data':data}, RequestContext(request))

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
   form = form.save()
   form.save()
 form = StnForm()
 return render_to_response('app/line.html',{'form':form}, RequestContext(request))

def Populate(request):
 sku = request.GET.get('sku', None)
 stn = Station.objects.filter(SKU=sku)
 stn1 = stn.values('stn1')[0]['stn1']
 stn2 = stn.values('stn2')[0]['stn2']
 stn3 = stn.values('stn3')[0]['stn3']
 stn4 = stn.values('stn4')[0]['stn4']
 stn5 = stn.values('stn5')[0]['stn5']
 stn6 = stn.values('stn6')[0]['stn6']
 stn7 = stn.values('stn7')[0]['stn7']
 stn8 = stn.values('stn8')[0]['stn8']
 stn9 = stn.values('stn9')[0]['stn9']
 stn10 = stn.values('stn10')[0]['stn10']
 data = {
     'stn1' : stn1,
     'stn2' : stn2,
     'stn3' : stn3,
     'stn4' : stn4,
     'stn5' : stn5,
     'stn6' : stn6,
     'stn7' : stn7,
     'stn8' : stn8,
     'stn9' : stn9,
     'stn10' : stn10,
     }
 return JsonResponse(data)
