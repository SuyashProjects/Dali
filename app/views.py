from django.shortcuts import render_to_response,redirect,render
from django.utils import timezone
from .models import Config,Constraint
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import Form1,Form2
from django.http import JsonResponse

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
