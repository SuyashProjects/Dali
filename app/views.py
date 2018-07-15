from django.shortcuts import render_to_response,redirect,render,get_object_or_404
from django.template.loader import render_to_string
from .models import Constraint,Config,Seq,Station,Shift
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import Form1,Edit,Delete,Form2,Form3,StnForm
from django.http import JsonResponse
from django.db.models import Sum,Max,Count,Min
from gen import main

@csrf_exempt
def form1(request):
 data = dict()
 if request.method == 'POST':
  form=Form1(request.POST)
  if form.is_valid():
   Obj=form.cleaned_data
   model=Obj['model']
   variant=Obj['variant']
   color=Obj['color']
   if (Config.objects.filter(model=model,variant=variant,color=color).exists()):
    data = 'This configuration already exists.'
   else:
    form=form.save()
    form.save()
  else:
   data = 'Invalid Form'
 form = Form1()
 view = Config.objects.all().values()
 return render_to_response('app/form1.html',{'form':form,'view':view,'data':data},RequestContext(request))

@csrf_exempt
def edit(request):
 data = dict()
 if request.method == 'POST':
  form = Edit(request.POST)
  if form.is_valid():
   data['form_is_valid'] = True
   Obj = form.cleaned_data
   SKU = Obj['SKU']
   model = Obj['model']
   variant = Obj['variant']
   color = Obj['color']
   tank = Obj['tank']
   time = Obj['time']
   description = Obj['description']
   Config.objects.filter(SKU=SKU).update(model=model,variant=variant,color=color,tank=tank,time=time,description=description)
   view = Config.objects.all().values()
   data['sku_list'] = render_to_string('app/partial_list.html', {'view': view})
  else:
   data['form_is_valid'] = False
 else:
  form = Edit()
  context = {'form': form}
  data['html_form'] = render_to_string('app/edit_popup.html',context,request=request)
 return JsonResponse(data)

@csrf_exempt
def delete(request):
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
  form = Delete()
  context = {'form': form}
  data['html_form'] = render_to_string('app/delete_popup.html',context,request=request)
 return JsonResponse(data)

@csrf_exempt
def form2(request):
 if request.method == 'POST':
  form = Form2(request.POST)
  if form.is_valid():
   Obj = form.cleaned_data
   SKU = Obj['SKU']
   quantity = Obj['quantity']
   ratio = Obj['ratio']
   Config.objects.filter(SKU=SKU).update(quantity=quantity,ratio=ratio)
  else:
   print('Error')
 form = Form2()
 forms = Form3()
 view = Config.objects.all().values()
 return render_to_response( 'app/form2.html',{'form':form,'view':view,'forms':forms}, RequestContext(request))

def validate(request):
 data = dict()
 Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
 Total_Shift_Time=list(Shift.objects.aggregate(Sum('time')).values())[0]
 Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
 Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
 if(Total_Order>Capacity):
  data['Output'] = 'Capacity is being exceeded, Reduce orders!'
 else:
  data['Output'] = 'Orders are within capacity, Sequence can now be generated!'
 return JsonResponse(data)

def sequence(request):
 Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
 Ratio_Sum=list(Config.objects.aggregate(Sum('ratio')).values())[0]
 Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
 SKU_Count=list(Config.objects.aggregate(Count('SKU')).values())[0]
 tl = Station.objects.values_list('stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')
 tq = Config.objects.exclude(quantity=0).values_list('quantity',flat=True)
 tr = Config.objects.exclude(quantity=0).values_list('ratio',flat=True)
 tsku = Config.objects.exclude(quantity=0).values_list('SKU',flat=True)
 for i in range(0,SKU_Count):
  if Config.objects.filter(SKU=i+1,quantity=0,ratio=0).exists():
   SKU_Count=SKU_Count-1
 Div = list(Config.objects.aggregate(Min('quantity')).values())[0]
 Total_Shift_Time=list(Shift.objects.aggregate(Sum('time')).values())[0]
 Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
 if(Total_Order<Capacity):
  #List for Phase1
  P1_Obj=[]
  P1_Seq=[]
  P1_Config=[]
  Sequence1=[]
  #List for Phase2
  P2_Seq=[]
  P2_Config=[]
  SKU_val=[]
  Ratio_val=[]
  Sequenced=[]
  P2_Obj=[]
  Sequence2=[]
  #List for Color Blocking
  l1=[]
  l2=[]
  l3=[]
  l4=[]
  l5=[]
  l6=[]
  Sequence3=[]
  #Phase1
  for i in range(0,SKU_Count):
   Quant=Config.objects.filter(SKU=i+1).values('quantity')[0]['quantity']
   for y in range(0,Quant):
    P1_Obj.append(Config.objects.get(SKU=i+1))
  for x in range(0,Total_Order):
   if not (Seq.objects.filter(Sq_No=x+1).exists()):
    Seq.objects.get_or_create(Sq_No=x+1,SKU=P1_Obj[x])
    P1_Seq.append(Seq.objects.filter(Sq_No=x+1).values())
    P1_Config.append(Config.objects.filter(SKU=Seq.objects.filter(Sq_No=x+1).values('SKU_id')[0]['SKU_id']).values())
    Sequence1 = list(zip(P1_Seq, P2_Config))
  #Phase2
  for i in range(0,SKU_Count):
   SKU_val.append(Config.objects.filter(SKU=i+1).values('SKU')[0]['SKU'])
   Ratio_val.append(Config.objects.filter(SKU=i+1).values('ratio')[0]['ratio'])
  sku_ratio = list(zip(SKU_val,Ratio_val))
  for x in range(0,Total_Order//Ratio_Sum):
   for key,value in sku_ratio:
    for value in range(value):
     Sequenced.append(key)
  for value in Sequenced:
   P2_Obj.append(Config.objects.get(SKU=value))
  for x in range(0,Total_Order):
   Seq.objects.filter(Sq_No=x+1).update(SKU=P2_Obj[x])
   P2_Seq.append(Seq.objects.filter(Sq_No=x+1).values())
   P2_Config.append(Config.objects.filter(SKU=Seq.objects.filter(Sq_No=x+1).values('SKU_id')[0]['SKU_id']).values())
   Sequence2 = list(zip(P2_Seq, P2_Config))
  #Color Blocking
  Color_Blocked=Config.objects.exclude(quantity=0,ratio=0).values('SKU').order_by('color')
  for key in Color_Blocked:
   l1.append(key['SKU'])
  for i in l1:
   l2.append(Config.objects.filter(SKU=i).values('ratio')[0]['ratio'])
  Color_Blocked = list(zip(l1, l2))
  for x in range (0,Total_Order//Ratio_Sum):
   for key,value in Color_Blocked:
    for value in range(value):
     l3.append(key)
  time = main(l3,tq,tl)
  for value in l3:
   l6.append(Config.objects.get(SKU=value))
  for x in range(0,Total_Order):
   Seq.objects.filter(Sq_No=x+1).update(SKU=l6[x])
   l4.append(Seq.objects.filter(Sq_No=x+1).values())
   l5.append(Config.objects.filter(SKU=Seq.objects.filter(Sq_No=x+1).values('SKU_id')[0]['SKU_id']).values())
   Sequence3 = list(zip(l4, l5))
 return render_to_response( 'app/sequence.html',{'Sequence1':Sequence1,'Sequence2':Sequence2,'Sequence3':Sequence3}, RequestContext(request))

def start(request):
 Sq_No = request.GET.get('Sq_No', None)
 Seq.objects.filter(Sq_No=Sq_No).update(status='Running')
 view =  Seq.objects.filter(SKU_id=sku).values('status')
 print(view)
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
 return render_to_response('app/Line.html',{'form':form}, RequestContext(request))

def populate(request):
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
