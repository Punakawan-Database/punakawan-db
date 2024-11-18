from django.shortcuts import render


def mypay(request):
    return render(request, "mypay.html")


def mypay_transaksi(request):
    return render(request, "mypay_transaksi.html")
