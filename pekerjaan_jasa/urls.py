from django.urls import path

from pekerjaan_jasa.views import pekerjaan_jasa, pekerjaan_jasa_status

app_name = "pekerjaan_jasa"

urlpatterns = [
    path("pekerjaan-jasa/", pekerjaan_jasa, name="pekerjaan_jasa"),
    path("pekerjaan-jasa/status/", pekerjaan_jasa_status, name="pekerjaan_jasa_status"),
]
