from django.shortcuts import render_to_response,redirect,render
from django.utils import timezone
from .models import Config,Constraint,Shift,Station
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import Form1,Form2
from django.http import JsonResponse
from django.db.models import Sum,Max,Count,Min

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
    view = Config.objects.all().values()
    return render_to_response( 'app/form2.html',{'form':form,'view':view}, RequestContext(request))

def sequence(request):
    Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
    Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
    SKU_Count=list(Config.objects.aggregate(Count('SKU')).values())[0]
    Div = list(Config.objects.aggregate(Min('quantity')).values())[0]
    Total_Shift_Time=8
    Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
    if(Total_Order>Capacity):
      print('Capacity is being exceeded, reduce orders!')
    else:
      print('Orders are within Capacity, Sequencing can now be started!')
      Seq_Num=[]
      Seq_SKU=[]
      Sequence={}
      Ratio1=1
      Ratio2=3
      Ratio_Sum=4
      SKU1=1
      SKU2=2
      Seq=[]
      temp=[]
      SKU_temp=[]
      for x in range (0,Total_Order//Ratio_Sum):
        for y in range(0,Ratio1):
         Seq.append(SKU1)
        for y in range(0,Ratio2):
         Seq.append(SKU2)
      for value in Seq:
          b=Config.objects.filter(SKU=value).values()
          temp.append(b)
      for i in range(0,SKU_Count):
          SKU=Config.objects.filter(SKU=i+1).values()
          query=Config.objects.filter(SKU=i+1).values('quantity')[0]
          Quant = query['quantity']
          for x in range(0,Total_Order):
           Seq_Num.append(x+1)
          for x in range(0,Quant):
              Seq_SKU.append(SKU)
          Sequence = list(zip(Seq_Num,Seq_SKU))
      Seq = list(zip(Seq_Num,temp))
    return render_to_response( 'app/sequence.html',{'Sequence':Sequence,'Seq':Seq}, RequestContext(request))

def populate(request):
    sku = request.GET.get('sku', None)
    view = Config.objects.filter(SKU=sku).values()
    return render_to_response( 'app/populate.html',{'view':view}, RequestContext(request))

def populate_variant(request):
    model = request.GET.get('model', None)
    view = Config.objects.filter(model=model).values()
    return render_to_response( 'app/variant.html',{'view':view}, RequestContext(request))

def populate_color(request):
    model = request.GET.get('model', None)
    variant = request.GET.get('variant', None)
    view = Config.objects.filter(model=model,variant=variant).values()
    return render_to_response( 'app/color.html',{'view':view}, RequestContext(request))

def populate_tank(request):
    model = request.GET.get('model', None)
    variant = request.GET.get('variant', None)
    color = request.GET.get('color', None)
    view = Config.objects.filter(model=model,variant=variant,color=color).values()
    return render_to_response( 'app/tank.html',{'view':view}, RequestContext(request))
