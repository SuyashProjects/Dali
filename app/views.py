from django.shortcuts import render_to_response,redirect,render,get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from .models import Constraint,Config,Seq,Station,Shift
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import Form1,Edit,Delete,Form2,Form3,StnForm
from django.http import JsonResponse
from django.db.models import Sum,Max,Count,Min
from django.core import serializers
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
   print('Invalid Form')
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
    tq = Config.objects.exclude(quantity__isnull=True).values_list('quantity',flat=True)
    tr = Config.objects.exclude(quantity__isnull=True).values_list('ratio',flat=True)
    tsku = Config.objects.exclude(quantity__isnull=True).values_list('SKU',flat=True)
    for i in range(0,SKU_Count):
     if Config.objects.filter(SKU=i+1,quantity=None,ratio=0).exists():
         SKU_Count=SKU_Count-1
    Div = list(Config.objects.aggregate(Min('quantity')).values())[0]
    Total_Shift_Time=list(Shift.objects.aggregate(Sum('time')).values())[0]
    Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
    if(Total_Order>Capacity):
      print('Capacity is being exceeded, reduce orders!')
    else:
      print('Orders are within Capacity, Sequencing can now be started!')
      Seq_Num=[]
      Seq_SKU=[]
      Sequence1={}
      Sequence2=[]
      Sequence3=[]
      sku_list=[]
      ratio_list=[]
      temp=[]
      list1=[]
      list2=[]
      full=[]
      #Color Blocking
      SKU5=Config.objects.exclude(quantity__isnull=True,ratio__isnull=True).values('SKU').order_by('color')
      for key in SKU5:
       list1.append(key['SKU'])
      for i in list1:
       list2.append(Config.objects.filter(SKU=i).values('ratio')[0]['ratio'])
      SKU5 = list(zip(list1, list2))
      for x in range (0,Total_Order//Ratio_Sum):
       for key,value in SKU5:
        for value in range(value):
         Sequence3.append(key)
      for value in Sequence3:
         full.append(Config.objects.filter(SKU=value).values())
      #Phase 1
      for i in range(0,SKU_Count):
       SKU=Config.objects.filter(SKU=i+1).values()
       Quant=Config.objects.filter(SKU=i+1).values('quantity')[0]['quantity']
       sku_list.append(Config.objects.filter(SKU=i+1).values('SKU')[0]['SKU'])
       ratio_list.append(Config.objects.filter(SKU=i+1).values('ratio')[0]['ratio'])
       for x in range(0,Total_Order):
        Seq_Num.append(x+1)
       for x in range(0,Quant):
        Seq_SKU.append(SKU)
      Sequence1 = list(zip(Seq_Num,Seq_SKU))
      Seq_SKU = list(zip(sku_list, ratio_list))
      #Phase 2
      for x in range (0,Total_Order//Ratio_Sum):
       for key,value in Seq_SKU:
        for value in range(value):
         Sequence2.append(key)
      for value in Sequence2:
         temp.append(Config.objects.filter(SKU=value).values())
      time = main(Sequence3,tq,tl)
      Sequence2 = list(zip(Seq_Num,temp))
      Sequence3 = list(zip(Seq_Num,full))

    return render_to_response( 'app/sequence.html',{'Sequence1':Sequence1,'Sequence2':Sequence2,'Sequence3':Sequence3}, RequestContext(request))

def start(request):
    sku = request.GET.get('sku', None)
    query = Config.objects.filter(SKU=sku).update(status='Running')
    context = {'data': query}
    data['html_form'] = render_to_string('app/edit_popup.html',context,request=request)

@csrf_exempt
def Line(request):
 if request.method == 'POST':
   form = StnForm(request.POST)
   if form.is_valid():
    form = form.save()
    form.save()
 form = StnForm()
 return render_to_response('app/Line.html',{'form':form}, RequestContext(request))
 return JsonResponse(data)

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
