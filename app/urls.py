from django.conf.urls import url,include
from . import views

urlpatterns=[
url(r'^$', views.Configuration, name='Configuration'),
url(r'^ajax/edit/$', views.Edit, name='Edit'),
url(r'^ajax/delete/$', views.Delete, name='Delete'),
url(r'^production/$', views.Production, name='Production'),
url(r'^ajax/validate/$', views.Validate, name='Validate'),
url(r'^sequence/$', views.Sequence, name='Sequence'),
url(r'^sequence/optimize/$', views.Optimize, name='Optimize'),
url(r'^ajax/start/$', views.Start, name='Start'),
url(r'^line/$', views.Line, name='Line'),
url(r'^ajax/populate/$', views.Populate, name='Populate'),
]
