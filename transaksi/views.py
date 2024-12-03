from django.http import Http404
from django.shortcuts import render

from utils import db

logged_user = {
    "id": "65ae2c07-9011-4a53-bd88-73a6b577691d",
    "role": "pekerja",
    "nama": "Jhon Doe",
}

# logged_user = {
#     "id": "fasdfasdfa-9011-4a53-bd88-73a6b577691d",
#     "role": "pengguna",
#     "nama": "Jono Doe",
# }

# context = {
#     "user": {
#         "role": "pengguna",
#         "nama": "John Doe",
#         "no_hp": "085172239073",
#         "saldo": 1000000000,
#     },
#     "transaksi": [
#         {
#             "nominal": 10000,
#             "tanggal": "19-10-1969",
#             "kategori": "TopUp MyPay",
#         }
#     ],
# }


def mypay(request):
    curr_user = logged_user
    # curr_user = request.session.get("user")

    user_result = db.query_one(
        """
        SELECT
            p.nama AS nama,
            p.nohp AS no_hp,
            p.saldomypay AS saldo
        FROM pengguna p
        WHERE p.id = %s
        """,
        [curr_user["id"]],
    )

    if user_result is None:
        raise Http404("User not found")

    transactions_result = db.query_all(
        """
        SELECT
            tr.tgl AS tanggal,
            tr.nominal AS nominal,
            ktr.nama AS kategori,
            CASE
                WHEN ktr.nama IN ('Topup', 'Honor Jasa') THEN TRUE
                ELSE FALSE
            END AS is_pemasukan
        FROM TR_MYPAY tr
            JOIN KATEGORI_TR_MYPAY ktr ON ktr.id = tr.kategoriid
        WHERE tr.userid = %s
        ORDER BY tr.tgl DESC
        """,
        [curr_user["id"]],
    )

    context = {
        "user": {
            "role": curr_user["role"],
            "nama": user_result["nama"],
            "no_hp": user_result["no_hp"],
            "saldo": user_result["saldo"],
        },
        "transaksi": transactions_result,
    }

    return render(request, "mypay.html", context)


def mypay_transaksi(request):
    context = {
        "user": {
            "role": "pengguna",
            "nama": "John Doe",
            "no_hp": "085172239073",
            "saldo": 1000000000,
        },
        "bank": [
            {
                "id": 1,
                "nama": "BCA",
            },
            {
                "id": 1,
                "nama": "BNI",
            },
            {
                "id": 1,
                "nama": "BRI",
            },
            {
                "id": 1,
                "nama": "MANDIRI",
            },
            {
                "id": 1,
                "nama": "Cimb Niaga",
            },
        ],
        "jasa": [
            {
                "id": 1,
                "nama": "Setrika",
                "harga": 20000,
            },
            {
                "id": 2,
                "nama": "Cuci Baju",
                "harga": 30000,
            },
            {
                "id": 3,
                "nama": "Bersih Kamar",
                "harga": 40000,
            },
            {
                "id": 4,
                "nama": "Sapu Halaman",
                "harga": 50000,
            },
        ],
    }
    return render(request, "mypay_transaksi.html", context)
