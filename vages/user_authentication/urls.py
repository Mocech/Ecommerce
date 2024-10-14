from django.urls import path
from . import views

app_name = 'user_authentication'

urlpatterns = [
    path('register/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),  # Changed to user_login
    path('logout/', views.logout, name='logout'),
]
