from django.urls import *;
from . import views;

urlpatterns = [
    path("", views.homepage, name="homepage"),
    
    path('subkategori/<str:kategori_slug>/<str:subkategori_slug>/',
        views.subkategori_jasa,
        name='subkategori_jasa'),
    
    path('subkategori2/<str:kategori_slug>/<str:subkategori_slug>/',
        views.subkategori_jasa_pekerja,
        name='subkategori_jasa_pekerja'),
    
    path('pemesanan_jasa/',
        views.view_pemesanan,
        name='view_pemesanan'),
    
    path('bergabung/<str:kategori>/',
        views.bergabung,
        name='bergabung'),
    # path('vd/',
    #     views.verify_discount,
    #     name='vd'),
    
    path('pesan/<str:idKategoriJasa>/<str:Sesi>/<str:idMetodeBayar>/<int:price>/',
        views.pesan,
        name='pesan'),
    
    path('pesan/<str:idKategoriJasa>/<str:Sesi>/<str:idMetodeBayar>/<int:price>/<str:idDiskon>/',
        views.pesan,
        name='pesan'),
]
