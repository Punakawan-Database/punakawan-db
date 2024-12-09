from django.urls import path
from . import views

urlpatterns = [
    path('', views.diskon, name='diskon'),
    path('beli_voucher/<str:kode>/<str:idmetode>/<str:tglakhir>/', views.beli_voucher, name='beli_voucher'),
]