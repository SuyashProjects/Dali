from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Config,Seq,Shift
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
    data='<span style="color:green">Sequence SKU added. Go to Line Monitoring to configure station TAKT times.</span>'
   else:
    data='<span style="color:red">This configuration already exists.</span>'
    form=SKUForm()
    view=Config.objects.all().values()
    return render(request,'app/configuration.html',{'form':form,'data':data,'view':view,})
  else:
   data='<span style="color:red">Invalid Configuration</span>'
   form=SKUForm(request.POST)
   view=Config.objects.all().values()
   return render(request,'app/configuration.html',{'form':form,'data':data,'view':view,})
 form=SKUForm()
 data=''
 view=Config.objects.all().values()
 return render(request,'app/configuration.html',{'form':form,'data':data,'view':view,})

@csrf_exempt
def Edit(request):
 data=dict()
 if request.method == 'POST':
  form=EditForm(request.POST)
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
   if Config.objects.filter(SKU=SKU).exists():
    Config.objects.filter(SKU=SKU).update(model=model,variant=variant,color=color,tank=tank,time=time,description=description,stn1=time,stn2=time,stn3=time,stn4=time,stn5=time,stn6=time,stn7=time,stn8=time,stn9=time,stn10=time)
   view=Config.objects.all().values()
   data['sku_list']=render_to_string('app/partial_list.html', {'view': view})
  else:
   data['form_is_valid'] = False
   form = EditForm(request.POST)
   context = {'form': form}
   data['html_form'] = render_to_string('app/edit_popup.html',context,request=request)
 else:
  form=EditForm()
  context={'form': form}
  data['html_form']=render_to_string('app/edit_popup.html',context,request=request)
 return JsonResponse(data)

@csrf_exempt
def Delete(request):
 data=dict()
 if request.method == 'POST':
  form=DeleteForm(request.POST)
  if form.is_valid():
   data['form_is_valid'] = True
   Obj=form.cleaned_data
   SKU=Obj['SKU']
   if Config.objects.filter(SKU=SKU).exists():
    Config.objects.filter(SKU=SKU).delete()
   view = Config.objects.all().values()
   data['sku_list'] = render_to_string('app/partial_list.html', {'view': view})
  else:
   data['form_is_valid'] = False
   form = DeleteForm(request.POST)
   context = {'form': form}
   data['html_form'] = render_to_string('app/delete_popup.html',context,request=request)
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
   if Config.objects.filter(SKU=SKU).exists():
    quantity = Obj['quantity']
    skips = Obj['skips']
    strips = Obj['strips']
    if (bool(Obj.get('ratio', False))):
     ratio = Obj['ratio']
    else:
     ratio = Obj['quantity']
    Config.objects.filter(SKU=SKU).update(quantity=quantity,ratio=ratio,skips=skips,strips=strips)
   else:
    form = OrderForm(request.POST)
    forms = ShiftForm()
    data='<span style="color:red">SKU does not exist.</span>'
    view = Config.objects.all().values()
    return render(request,'app/production.html',{'form':form,'forms':forms,'data':data,'view':view})
  else:
   form = OrderForm(request.POST)
   forms = ShiftForm()
   data='<span style="color:red">Invalid Order.</span>'
   view = Config.objects.all().values()
   return render(request,'app/production.html',{'form':form,'forms':forms,'data':data,'view':view})
 elif 'shift' in request.POST:
  forms = ShiftForm(request.POST)
  if forms.is_valid():
   Obj = forms.cleaned_data
   A = Obj['A']
   B = Obj['B']
   C = Obj['C']
   Shift.objects.filter(name='Shift').update(A=A,B=B,C=C)
   form = OrderForm()
   forms = ShiftForm()
   data='<span style="color:green">Successfully changed productive shift times.</span>'
   view = Config.objects.all().values()
   return render(request,'app/production.html',{'form':form,'forms':forms,'data':data,'view':view})
  else:
   form = OrderForm()
   forms = ShiftForm(request.POST)
   data='<span style="color:red">Invalid Shift Timings.</span>'
   view = Config.objects.all().values()
   return render(request,'app/production.html',{'form':form,'forms':forms,'data':data,'view':view})
 form = OrderForm()
 forms = ShiftForm()
 data =''
 view = Config.objects.all().values()
 return render(request,'app/production.html',{'form':form,'forms':forms,'data':data,'view':view})

def Validate(request):
 data=dict()
 Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
 Total_Shift_Time=list(Shift.objects.filter(name='Shift').values_list('A','B','C'))
 Total_Shift_Time=sum(Total_Shift_Time)
 Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
 Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
 if Total_Order>Capacity:
  data['Output'] = '<span style="color:red">Capacity is being exceeded, Reduce orders!</span>'
 else:
  data['Output'] = '<span style="color:green">Orders are within capacity, Sequence can now be generated!</span>'
 return JsonResponse(data)

def Sequence(request):
 Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
 Ratio_Sum=list(Config.objects.aggregate(Sum('ratio')).values())[0]
 Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
 SKU_Count=list(Config.objects.aggregate(Count('SKU')).values())[0]
 if Config.objects.filter(SKU__range=(0,SKU_Count),quantity=0).exists():
  SKU_Count=SKU_Count-1
 if SKU_Count==0:
  data='No Orders'
  Sequence=[]
  return render(request,'app/sequence.html',{'Sequence':Sequence,'data':data})
 Seq_Q=Seq.objects.all().count()
 forsub = Config.objects.exclude(quantity=0).values_list('SKU','quantity','ratio','skips','strips','stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')
 Sequence=sub(forsub,Total_Order)
 Total_Order=len(Sequence)
 tl = forsub.values_list('stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')
 Total_Shift_Time=list(Shift.objects.filter(name='Shift').values_list('A','B','C'))
 Total_Shift_Time=sum(Total_Shift_Time)
 Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
 if(Total_Order<Capacity):
  tSeq=[]
  P2_Obj=[]
  Seq.objects.filter(Sq_No__range=(Total_Order+1,Seq_Q)).delete()
  time = main(Sequence,tl,forsub)
  data = 'Time Taken: ' +str(time)+ ' minutes'
  for value in Sequence:
   if value==0:
    P2_Obj.append(0)
   else:
    P2_Obj.append(Config.objects.get(SKU=value))
  for x in range(0,Total_Order):
   if not Seq.objects.filter(Sq_No=x+1).exists():
    if P2_Obj[x]==0:
     Seq.objects.create(Sq_No=x+1)
    else:
     Seq.objects.create(Sq_No=x+1,SKU=P2_Obj[x])
   else:
    if P2_Obj[x]==0:
     Seq.objects.filter(Sq_No=x+1).update(SKU='')
    else:
     Seq.objects.filter(Sq_No=x+1).update(SKU=P2_Obj[x])
  Sequence=Seq.objects.values('Sq_No','SKU__SKU','SKU__model','SKU__variant','SKU__color','SKU__tank','status')
 else:
  data='<span style="color:red">Capacity is being exceeded, Reduce orders!<span>'
  Sequence=[]
  return render(request,'app/sequence.html',{'Sequence':Sequence,'data':data})
 return render(request,'app/sequence.html',{'Sequence':Sequence,'data':data})

def Optimize(request):
  tSeq=[]
  P3_Obj=[]
  Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
  Ratio_Sum=list(Config.objects.aggregate(Sum('ratio')).values())[0]
  forsub = Config.objects.exclude(quantity=0).values_list('SKU','quantity','ratio','skips','strips','stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10').order_by('color')
  Sequence=sub(forsub,Total_Order)
  tl = forsub.values_list('stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')
  time = main(Sequence,tl,forsub)
  data = 'Time Taken: ' +str(time)+ ' minutes'
  for value in Sequence:
   if value==0:
    P3_Obj.append(0)
   else:
    P3_Obj.append(Config.objects.get(SKU=value))
  for x in range(0,Total_Order):
   if P3_Obj[x]==0:
    Seq.objects.filter(Sq_No=x+1).update(SKU='')
   else:
    Seq.objects.filter(Sq_No=x+1).update(SKU=P3_Obj[x])
  Sequence=Seq.objects.values('Sq_No','SKU__SKU','SKU__model','SKU__variant','SKU__color','SKU__tank','status')
  return render(request,'app/sequence.html',{'Sequence':Sequence,'data':data})


def Start(request):
 data=dict()
 Sq_No = request.GET.get('Sq_No', None)
 Seq.objects.filter(Sq_No=Sq_No).update(status='Running')
 Sequence=Seq.objects.values('Sq_No','SKU__SKU','SKU__model','SKU__variant','SKU__color','SKU__tank','status')
 context = {'Sequence':Sequence}
 data['Sequence'] = render_to_string('app/partial_seq.html',context,request=request)
 return JsonResponse(data)

@csrf_exempt
def Line(request):
 if request.method == 'POST':
  form = StnForm(request.POST)
  if form.is_valid():
   Obj = form.cleaned_data
   SKU = Obj['SKU']
   if Config.objects.filter(SKU=SKU).exists():
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
    form = StnForm(request.POST)
    data = '<span style="color:red">SKU does not exist.</span>'
    return render(request,'app/line.html',{'form':form,'data':data})
  else:
   form = StnForm(request.POST)
   data = '<span style="color:red">Cannot Add,Invalid Station Timings</span>'
   return render(request,'app/line.html',{'form':form,'data':data})
 data=''
 form = StnForm()
 return render(request,'app/line.html',{'form':form,'data':data})

def Populate(request):
 data=dict()
 stn=[]
 SKU = request.GET.get('sku', None)
 if Config.objects.filter(SKU=SKU).exists():
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
   'Output' : '<span style="color:green">Success!</span>'
   }
 else:
  data['Output'] = '<span style="color:red">SKU does not exist.</span>'
 return JsonResponse(data)
