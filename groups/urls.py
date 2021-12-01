from django.urls import path
from . import  views

urlpatterns = [
    path('', views.index, name='index'),
    path('addphone', views.addphone, name='addphone'),
    path('phones', views.phones, name='phones'),
    path('<int:number>/reg', views.reg, name='reg'),
    path('<int:number>/info', views.info, name='info'),
    path('<int:number>/groups', views.chanels, name='groups'),
    path('<int:number>/addgroup', views.add_group, name='add_group'),
]