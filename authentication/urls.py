from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile-pelanggan/', views.profile_pelanggan, name='profile_pelanggan'),
    path('profile-pekerja/', views.profile_pekerja, name='profile_pekerja'),
    path('register-pelanggan/', views.register_pelanggan, name='register_pelanggan'),
    path('register-pekerja/', views.register_pekerja, name='register_pekerja'),
    path('update-pengguna/', views.update_pelanggan, name='update_pelanggan'),
    path('update-pekerja/', views.update_pekerja, name='update_pekerja'),
]
