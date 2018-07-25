from django.conf.urls import url
from theCraftMapsCO import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='homepage'),
    url(r'^home/$', views.home, name='homepage'),
    url(r'^routes/$', views.routes, name='routes'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^multiRoutes/$', views.multiRoutes, name='multiRoutes'),
    url(r'^brewery/(?P<name>.*)/$', views.brewery_page, name='brewery_page'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^user/$', views.user_page, name='user_page')
]

#url(r'^routes/(?P<start>\w+)/$', views.routes, name='routes'),