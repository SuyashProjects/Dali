from django.shortcuts import render_to_response,redirect,render
from django.utils import timezone
from .models import Config,Constraint,Shift,Station
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import Form1,Form2,Form3,Station
from django.http import JsonResponse
from django.db.models import Sum,Max,Count,Min
from gen import main

@csrf_exempt
def form1(request):
    if request.method == 'POST':
      form = Form1(request.POST)
      if form.is_valid():
          Obj = form.cleaned_data
          model = Obj['model']
          variant = Obj['variant']
          color = Obj['color']
          if (Config.objects.filter(model=model,variant=variant,color=color).exists()):
           print('sku exists')
          else:
           form = form.save()
           form.save()
    form = Form1()
    view = Config.objects.all().values()
    return render_to_response( 'app/form1.html',{'form':form, 'view':view}, RequestContext(request))

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

def sequence(request):
    Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
    Ratio_Sum=list(Config.objects.aggregate(Sum('ratio')).values())[0]
    Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
    SKU_Count=list(Config.objects.aggregate(Count('SKU')).values())[0]
    tl = Station.objects.values_list('stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')
    tq = Config.objects.exclude(quantity__isnull=True).values_list('quantity',flat=True)
    for i in range(0,SKU_Count):
     if Config.objects.filter(SKU=i+1,quantity=None,ratio=None).exists():
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

    return render_to_response( 'app/sequence.html',{'Sequence1':Sequence1,'Sequence2':Sequence2,'Sequence3':Sequence3,'time':time}, RequestContext(request))

@csrf_exempt
def Line(request):
 if request.method == 'POST':
   form = Station(request.POST)
   if form.is_valid():
    form = form.save()
    form.save()
 form = Station()
 return render_to_response( 'app/Line.html',{'form':form}, RequestContext(request))
