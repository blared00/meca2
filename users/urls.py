from django.urls import path

from .views import RegistrationAPIView
from .views import LoginAPIView

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='user_registration'),
    path('login/', LoginAPIView.as_view(), name='user_login'),
]