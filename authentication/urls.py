from authentication import views 
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('validate-username', csrf_exempt(views.UserNameValidationView.as_view()), name='validate_username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name='validate_email'), 
]
