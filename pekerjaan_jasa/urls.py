from django.urls import path

from pekerjaan_jasa.views import (
    pekerjaan_jasa,
    pekerjaan_jasa_status,
    pekerjaan_jasa_status_update,
    pekerjaan_jasa_update,
)

app_name = "pekerjaan_jasa"

urlpatterns = [
    path("pekerjaan-jasa/", pekerjaan_jasa, name="pekerjaan_jasa"),
    path("pekerjaan-jasa/update/", pekerjaan_jasa_update, name="pekerjaan_jasa_update"),
    path("pekerjaan-jasa/status/", pekerjaan_jasa_status, name="pekerjaan_jasa_status"),
    path(
        "pekerjaan-jasa/status/update/",
        pekerjaan_jasa_status_update,
        name="pekerjaan_jasa_status_update",
    ),
]
