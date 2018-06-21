from django.shortcuts import render_to_response,redirect,render
from django.utils import timezone
from .models import Config
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import Form1,Form2

@csrf_exempt
def form1(request):
    if request.method == 'POST':
      form = Form1(request.POST)
      if form.is_valid():
          Obj = form.cleaned_data
          model = Obj['model']
          variant = Obj['variant']
          color = Obj['color']
          if (Config.objects.filter(model=model).exists()):
            if (Config.objects.filter(variant=variant).exists()):
              if (Config.objects.filter(color=color).exists()):
                  print('sku exists')
              else:
                  form = form.save()
                  form.save()
            else:
                  form = form.save()
                  form.save()
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
    model = Config.objects.filter(sku=sku).only('model')
    variant = Config.objects.filter(sku=sku).only('varaint')
    color = Config.objects.filter(sku=sku).only('color')
    data = {
        'model' : model,
        'variant' : variant,
        'color' : color
        }
    return JsonResponse(data)
