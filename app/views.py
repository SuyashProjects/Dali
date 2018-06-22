from django.shortcuts import render_to_response,redirect,render
from django.utils import timezone
from .models import Config,Constraint
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import Form1,Form2
from django.http import JsonResponse
from django.db.models import Sum,Max

@csrf_exempt
def form1(request):
    if request.method == 'POST':
      form = Form1(request.POST)
      if form.is_valid():
          Obj = form.cleaned_data
          model = Obj['model']
          variant = Obj['variant']
          color = Obj['color']
          if (Config.objects.filter(model=model, variant=variant,color=color).exists()):
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
        form = form.save()
        form.save()
      else:
          print('error')
    form = Form2()
    return render_to_response( 'app/form2.html',{'form':form}, RequestContext(request))

def sequence(request):
    Total_Order=list(Config.objects.aggregate(Sum('quantity')).values())[0]
    Line_Takt_Time = list(Config.objects.aggregate(Max('time')).values())[0]
    Total_Shift_Time=8
    Capacity=((Total_Shift_Time*3600)/Line_Takt_Time)
    if(Total_Order>Capacity):
      print('Capacity is being exceeded, reduce orders!')
    else:
      print('Orders are within Capacity, Sequencing can now be started!')
      j=0
      Seq_Num=[Total_Order]
      Seq_SKU=[Total_Order]
      for i in range(1,Total_Order):
          SKU_Number=Config.objects.filter(SKU=i).values()
          query=Config.objects.filter(SKU=i).values('quantity')
          print(query)
          Quant = query['quantity']
          while Quant!=0:
              Seq_Num[j]=j+1
              Seq_SKU[j]=SKU_Number
              Quant=Quant-1
              j=j+1
    return render_to_response( 'app/sequence.html',{'Seq_Num':Seq_Num,'Seq_SKU':Seq_SKU}, RequestContext(request))

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
