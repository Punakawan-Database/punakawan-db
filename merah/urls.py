from django.urls import path

from merah.views import mypay, mypay_transaksi, pekerjaan_jasa, pekerjaan_jasa_status

app_name = "merah"

urlpatterns = [
    path("mypay", mypay, name="mypay"),
    path("mypay/transaksi", mypay_transaksi, name="mypay_transaksi"),
    path("pekerjaan-jasa", pekerjaan_jasa, name="pekerjaan_jasa"),
    path("pekerjaan-jasa-status", pekerjaan_jasa_status, name="pekerjaan_jasa_status"),
]
