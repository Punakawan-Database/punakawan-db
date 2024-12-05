from django.shortcuts import render
from datetime import datetime, timedelta

# Create your views here.
def diskon(request):
    voucher_data = [
        {
            'kode': 'DISC50',
            'potongan': '50%',
            'min_transaksi': 'Rp 100.000',
            'jumlah_hari': '30',
            'kuota': '100',
            'harga': 'Rp 25.000'
        },
        {
            'kode': 'SAVE25',
            'potongan': '25%',
            'min_transaksi': 'Rp 50.000',
            'jumlah_hari': '15',
            'kuota': '200',
            'harga': 'Rp 15.000'
        },
        {
            'kode': 'MEGA75',
            'potongan': '75%',
            'min_transaksi': 'Rp 200.000',
            'jumlah_hari': '7',
            'kuota': '50',
            'harga': 'Rp 45.000'
        }
    ]

    # Generate dummy data for promos
    # Creating actual dates for the next 3 months
    promo_data = [
        {
            'kode': 'NEWUSER2024',
            'tanggal_akhir': (datetime.now() + timedelta(days=30)).strftime('%d %B %Y')
        },
        {
            'kode': 'SPECIAL10',
            'tanggal_akhir': (datetime.now() + timedelta(days=60)).strftime('%d %B %Y')
        },
        {
            'kode': 'HOLIDAY24',
            'tanggal_akhir': (datetime.now() + timedelta(days=90)).strftime('%d %B %Y')
        }
    ]

    context = {
        'vouchers': voucher_data,
        'promos': promo_data,
    }
    
    return render(request, 'diskon.html', context)