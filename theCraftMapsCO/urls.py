from django.conf.urls import url
from theCraftMapsCO import views

urlpatterns = [
    url(r'^$', views.home, name='homepage'),
    url(r'^home/$', views.home, name='homepage'),
    url(r'^routes/$', views.routes, name='routes'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^mulroutes/$', views.mulroutes, name='mulroutes')
]