from django.shortcuts import render, redirect
from django.urls import *
from utils import db;

from django.contrib.auth import get_user
from json import dumps 
import requests
from datetime import datetime, timedelta

# Create your views here.
def diskon(request):
    voucher_data = db.query_all("SELECT * FROM voucher JOIN diskon ON voucher.kode = diskon.kode")
    promo_data = db.query_all("SELECT * FROM promo JOIN diskon ON promo.kode = diskon.kode")
    metode_bayar = db.query_all("SELECT * FROM metode_bayar")

    context = {
        'vouchers': voucher_data,
        'promos': promo_data,
        'metode_bayar': metode_bayar
    }
    
    return render(request, 'diskon.html', context)

