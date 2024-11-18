from django.shortcuts import render


def mypay(request):
    context = {
        "user": {
            "role": "pengguna",
            "nama": "John Doe",
            "no_hp": "085172239073",
            "saldo": 1000000000,
        },
        "transaksi": [
            {
                "nominal": 10000,
                "tanggal": "19-10-1969",
                "kategori": "TopUp MyPay",
            },
            {
                "nominal": 20000,
                "tanggal": "20-10-1969",
                "kategori": "Pembayaran Transaksi",
            },
            {
                "nominal": 15000,
                "tanggal": "21-10-1969",
                "kategori": "Transfer MyPay",
            },
            {
                "nominal": 5000,
                "tanggal": "22-10-1969",
                "kategori": "Withdrawal",
            },
            {
                "nominal": 25000,
                "tanggal": "23-10-1969",
                "kategori": "TopUp MyPay",
            },
            {
                "nominal": 30000,
                "tanggal": "24-10-1969",
                "kategori": "Pembayaran Transaksi",
            },
            {
                "nominal": 12000,
                "tanggal": "25-10-1969",
                "kategori": "Transfer MyPay",
            },
            {
                "nominal": 8000,
                "tanggal": "26-10-1969",
                "kategori": "Withdrawal",
            },
            {
                "nominal": 18000,
                "tanggal": "27-10-1969",
                "kategori": "TopUp MyPay",
            },
            {
                "nominal": 22000,
                "tanggal": "28-10-1969",
                "kategori": "Pembayaran Transaksi",
            },
            {
                "nominal": 17000,
                "tanggal": "29-10-1969",
                "kategori": "Transfer MyPay",
            },
            {
                "nominal": 9000,
                "tanggal": "30-10-1969",
                "kategori": "Withdrawal",
            },
            {
                "nominal": 26000,
                "tanggal": "31-10-1969",
                "kategori": "TopUp MyPay",
            },
            {
                "nominal": 14000,
                "tanggal": "01-11-1969",
                "kategori": "Pembayaran Transaksi",
            },
            {
                "nominal": 11000,
                "tanggal": "02-11-1969",
                "kategori": "Transfer MyPay",
            },
            {
                "nominal": 7000,
                "tanggal": "03-11-1969",
                "kategori": "Withdrawal",
            },
        ],
    }
    return render(request, "mypay.html", context)


def mypay_transaksi(request):
    return render(request, "mypay_transaksi.html")
