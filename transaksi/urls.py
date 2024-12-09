from django.urls import path

from transaksi.views import (
    mypay,
    mypay_transaksi,
    mypay_transaksi_bayar,
    mypay_transaksi_topup,
    mypay_transaksi_transfer,
    mypay_transaksi_withdraw,
)

app_name = "transaksi"

urlpatterns = [
    path("mypay/", mypay, name="mypay"),
    path("mypay/transaksi/", mypay_transaksi, name="mypay_transaksi"),
    path("mypay/transaksi/topup", mypay_transaksi_topup, name="mypay_transaksi_topup"),
    path("mypay/transaksi/bayar", mypay_transaksi_bayar, name="mypay_transaksi_bayar"),
    path("mypay/transaksi/transfer", mypay_transaksi_transfer, name="mypay_transaksi_transfer"),
    path("mypay/transaksi/withdraw", mypay_transaksi_withdraw, name="mypay_transaksi_withdraw"),
]
