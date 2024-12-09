from django.shortcuts import render, redirect
from django.urls import *
from utils import db;

from django.contrib.auth import get_user
from json import dumps 
import requests
from datetime import datetime, timedelta

# Create your views here.
def diskon(request):
    idUser = request.session.get('user_id')
    saldo = db.query_one("SELECT saldomypay FROM pengguna WHERE id = %s", (idUser,))['saldomypay']
    voucher_data = db.query_all("SELECT * FROM voucher JOIN diskon ON voucher.kode = diskon.kode")
    promo_data = db.query_all("SELECT * FROM promo JOIN diskon ON promo.kode = diskon.kode")
    metode_bayar = db.query_all("SELECT * FROM metode_bayar")

    context = {
        'vouchers': voucher_data,
        'promos': promo_data,
        'metode_bayar': metode_bayar,
        'saldo': saldo,
    }
    
    return render(request, 'diskon.html', context)

def beli_voucher(request, kode, idmetode, tglakhir):
    tglawal = datetime.now()
    idUser = request.session.get('user_id')
    price = db.query_one("SELECT harga FROM voucher WHERE kode = %s", (kode,))['harga']
    db.query_one("UPDATE pengguna SET saldomypay = saldomypay - %s WHERE id = %s", (price, idUser))
    db.query_one("INSERT INTO TR_PEMBELIAN_VOUCHER VALUES (uuid_generate_v4(), %s, %s, 0, (SELECT Id from PELANGGAN WHERE Id = %s), %s, (SELECT Id from METODE_BAYAR WHERE NAMA = %s))", (tglawal, tglakhir, idUser, kode, idmetode))
    return redirect('diskon')