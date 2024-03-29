"""dprojx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from dappx import views
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views as v
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^special/',views.special,name='special'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
    path(r'api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^dappx/', include('dappx.urls')),
    url(r'^chatapp/', include('chatapp.urls')),
]