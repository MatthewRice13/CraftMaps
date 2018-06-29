"""CraftMaps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from theCraftMapsCO import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('theCraftMapsCO.urls')),
    url(r'^home/', include('theCraftMapsCO.urls')),
    url(r'^routes/', include('theCraftMapsCO.urls')),
    url(r'^about/', include('theCraftMapsCO.urls')),
    url(r'^contact/', include('theCraftMapsCO.urls')),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)