from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.form1, name='form1'),
    url(r'^form2/$', views.form2, name='form2'),
    url(r'^ajax/populate/$', views.populate, name='populate'),
    url(r'^ajax/populate_variant/$', views.populate_variant, name='populate_variant'),
    url(r'^ajax/populate_color/$', views.populate_color, name='populate_color'),
    url(r'^ajax/populate_tank/$', views.populate_tank, name='populate_tank'),
]
