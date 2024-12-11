# compartido/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import HomeView, CustomLoginView, no_permission #check_message

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('no-permission/', no_permission, name='no_permission'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Añadido el LogoutView
   # path('check-message/', check_message, name='check_message'),
]
