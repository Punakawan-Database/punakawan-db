from django.urls import path

from transaksi.views import mypay, mypay_transaksi

app_name = "transaksi"

urlpatterns = [
    path("mypay/", mypay, name="mypay"),
    path("mypay/transaksi/", mypay_transaksi, name="mypay_transaksi"),
]
