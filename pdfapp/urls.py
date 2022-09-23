from distutils.log import Log
from django.urls import path
from knox.views import LogoutView as KnoxLogoutView
from .views import RegisterAPI, LoginAPI, ValidateAPI, PasswordResetAPI, GuestAPI, DocumentUploadAPI, DocumentsViewAPI, DocumentPageVisitAPIView
from .views import GuestVisitsViewAPI

urlpatterns = [
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/logout/', KnoxLogoutView.as_view(), name='logout'),
    path('api/validate/<str:username>/', ValidateAPI.as_view(), name="validate"),
    path('api/reset/', PasswordResetAPI.as_view(), name='reset'),
    path('api/guest/', GuestAPI.as_view(), name='guest'),
    path('api/upload/', DocumentUploadAPI.as_view(), name='upload'),
    path('api/documents/', DocumentsViewAPI.as_view(), name='documents'),
    path('api/guests/visits/', GuestVisitsViewAPI.as_view(), name="guests_views"),
    path('api/guests/page/visits/', DocumentPageVisitAPIView.as_view(), name="page_visits")
]