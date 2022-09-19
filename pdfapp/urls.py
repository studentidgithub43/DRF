from distutils.log import Log
from django.urls import path
from .views import RegisterAPI, LoginAPI
from knox.views import LogoutView as KnoxLogoutView

urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/logout/', KnoxLogoutView.as_view(), name='logout')
]