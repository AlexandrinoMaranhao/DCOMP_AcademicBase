from django.urls import path
from .views import UserRegistrationView, LoginView, LogoutView

urlpatterns = [
    path('registro/', UserRegistrationView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
