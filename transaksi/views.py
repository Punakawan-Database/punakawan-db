from django.http import Http404
from django.shortcuts import render

from utils import db

# logged_user = {
#     "id": "65ae2c07-9011-4a53-bd88-73a6b577691d",
#     "role": "pekerja",
#     "nama": "Jhon Doe",
# }

logged_user = {
    "id": "d02eee9e-83a4-4e42-9ffe-3defcab6d447",
    "role": "pelanggan",
    "nama": "Jono Doe",
}

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

# context = {
#     "user": {
#         "role": "pengguna",
#         "nama": "John Doe",
#         "no_hp": "085172239073",
#         "saldo": 1000000000,
#     },
#     "bank": [
#         {
#             "id": 1,
#             "nama": "BCA",
#         }
#     "jasa": [
#         {
#             "id": 1,
#             "nama": "Setrika",
#             "harga": 20000,
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
        FROM PENGGUNA p
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
    curr_user = logged_user
    # curr_user = request.session.get("user")

    user_result = db.query_one(
        """
        SELECT
            p.nama AS nama,
            p.nohp AS no_hp,
            p.saldomypay AS saldo
        FROM PENGGUNA p
        WHERE p.id = %s
        """,
        [curr_user["id"]],
    )

    if user_result is None:
        raise Http404("User not found")

    context = {
        "user": {
            "role": curr_user["role"],
            "nama": user_result["nama"],
            "no_hp": user_result["no_hp"],
            "saldo": user_result["saldo"],
        },
    }

    if curr_user["role"] == "pelanggan":
        jasa_results = db.query_all(
            """
            SELECT
                skj.id AS id,
                skj.namasubkategori AS nama,
                tpj.tglpemesanan AS tgl,
                tpj.totalbiaya AS total_biaya
            FROM TR_PEMESANAN_JASA tpj
                JOIN PELANGGAN pl
                    ON pl.id = tpj.idpelanggan
                JOIN SESI_LAYANAN sl
                    ON sl.sesi = tpj.sesi AND sl.subkategoriid = tpj.idkategorijasa
                JOIN SUBKATEGORI_JASA skj
                    ON skj.id = sl.subkategoriid
            WHERE pl.id = %s
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
            "jasa": jasa_results,
        }

    return render(request, "mypay_transaksi.html", context)
