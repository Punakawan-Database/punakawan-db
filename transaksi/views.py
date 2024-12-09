import uuid

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from utils import db

# logged_user = {
#     "id": "65ae2c07-9011-4a53-bd88-73a6b577691d",
#     "role": "pekerja",
#     "nama": "Jhon Doe",
# }

logged_user = {
    "id": "c805f812-a271-4ad1-b063-901bb0bc9bfe",
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
                JOIN TR_PEMESANAN_STATUS tps
                    ON tps.idtrpemesanan = tpj.id
                JOIN STATUS_PESANAN sp
                    ON sp.id = tps.idstatus
                JOIN (
                    SELECT
                        idtrpemesanan,
                        MAX(tglwaktu) AS tglwaktu
                    FROM TR_PEMESANAN_STATUS
                    GROUP BY idtrpemesanan
                ) tps_latest
                    ON tps_latest.idtrpemesanan = tps.idtrpemesanan
                    AND tps_latest.tglwaktu = tps.tglwaktu
            WHERE
                sp.status = 'Menunggu Pembayaran'
                AND pl.id = %s
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
            "bank": ["BCA", "BNI", "BRI", "Mandiri", "Bank Jateng"],
        }

    return render(request, "mypay_transaksi.html", context)


@require_POST
def mypay_transaksi_topup(request):
    curr_user = logged_user
    # curr_user = request.session.get("user")

    # Get and validate nominal
    nominal = request.POST.get("nominal")
    if not nominal:
        messages.error(request, "nominal topup harus diisi")
        return redirect("transaksi:mypay_transaksi")

    # Convert to float and validate
    try:
        nominal = float(nominal)
    except ValueError:
        messages.error(request, "nominal topup harus berupa angka")
        return redirect("transaksi:mypay_transaksi")

    # Business rules validation
    if nominal <= 0:
        messages.error(request, "nominal topup harus lebih dari 0")
        return redirect("transaksi:mypay_transaksi")

    user_transaction = db.query_one(
        """
        INSERT INTO TR_MYPAY (id, userid, tgl, nominal, kategoriid)
        VALUES (%s, %s, NOW(), %s, (SELECT id FROM KATEGORI_TR_MYPAY WHERE nama = 'Topup'))
        RETURNING *
        """,
        [uuid.uuid4(), curr_user["id"], nominal],
    )

    if not user_transaction:
        messages.error(request, "gagal melakukan top up: transaksi tidak tercatat")
        return redirect("transaksi:mypay_transaksi")

    updated_user = db.query_one(
        """
        UPDATE PENGGUNA
        SET saldomypay = saldomypay + %s
        WHERE id = %s
        RETURNING *
        """,
        [nominal, curr_user["id"]],
    )

    if not updated_user:
        messages.error(request, "Gagal memperbarui saldo")
        return redirect("transaksi:mypay_transaksi")

    return redirect("transaksi:mypay")


@require_POST
def mypay_transaksi_bayar(request):
    curr_user = logged_user
    # curr_user = request.session.get("user")

    order_id = request.POST.get("jasa_id")
    harga = request.POST.get("harga")

    # Update user balance
    db.query_one(
        """
        UPDATE PENGGUNA
        SET saldomypay = saldomypay - %s
        WHERE id = %s
        """,
        [harga, curr_user["id"]],
    )

    # Log transaction
    db.query_one(
        """
        INSERT INTO TR_MYPAY
        (userid, nominal, kategoriid, tgl)
        VALUES
        (%s, %s, (SELECT id FROM KATEGORI_TR_MYPAY WHERE nama = 'Pembayaran Jasa'), NOW())
        """,
        [curr_user["id"], harga],
    )

    return redirect("transaksi:mypay")


@require_POST
def mypay_transaksi_transfer(request):
    curr_user = logged_user
    # curr_user = request.session.get("user")

    no_hp = request.POST.get("no_hp")
    nominal = request.POST.get("nominal")

    # Get target user
    target_user = db.query_one(
        """
        SELECT p.id
        FROM PENGGUNA p
        WHERE p.nohp = %s"
        """,
        [no_hp],
    )

    # Update riwayat transaksi sender
    db.query_one(
        """
        INSERT INTO TR_MYPAY (userid, nominal, kategoriid, tgl)
        VALUES (%s, %s, (SELECT id FROM KATEGORI_TR_MYPAY WHERE nama = 'Transfer'), NOW())
        """,
        [curr_user["id"], nominal],
    )

    # Update riwayat transaksi receiver
    db.query_one(
        """
        INSERT INTO TR_MYPAY (userid, nominal, kategoriid, tgl)
        VALUES (%s, %s, (SELECT id FROM KATEGORI_TR_MYPAY WHERE nama = 'Transfer'), NOW())
        """,
        [curr_user["id"], nominal],
    )

    # Update saldo sender
    db.query_one(
        """
        UPDATE PENGGUNA p
        SET p.saldomypay = p.saldomypay - %s
        WHERE p.id = %s
        """,
        [nominal, curr_user["id"]],
    )

    # Update saldo receiver
    db.query_one(
        """
        UPDATE PENGGUNA p
        SET p.saldomypay = p.saldomypay + %s
        WHERE p.id = %s
        """,
        [nominal, curr_user["id"]],
    )

    return redirect("transaksi:mypay")


@require_POST
def mypay_transaksi_withdraw(request):
    curr_user = logged_user
    # curr_user = request.session.get("user")

    # Get and validate nominal
    nominal = request.POST.get("nominal")
    if not nominal:
        messages.error(request, "nominal withdraw harus diisi")
        return redirect("transaksi:mypay_transaksi")

    # Convert to float and validate
    try:
        nominal = float(nominal)
    except ValueError:
        messages.error(request, "nominal withdraw harus berupa angka")
        return redirect("transaksi:mypay_transaksi")

    # Business rules validation
    if nominal <= 0:
        messages.error(request, "nominal withdraw harus lebih dari 0")
        return redirect("transaksi:mypay_transaksi")

    # Check current balance
    current_balance = db.query_one(
        """
        SELECT saldomypay
        FROM PENGGUNA
        WHERE id = %s
        """,
        [curr_user["id"]],
    )

    if not current_balance or current_balance["saldomypay"] < nominal:
        messages.error(request, "saldo tidak mencukupi")
        return redirect("transaksi:mypay_transaksi")

    withdrawal = db.query_one(
        """
        INSERT INTO TR_MYPAY (id, userid, tgl, nominal, kategoriid)
        VALUES (%s, %s, NOW(), %s, (SELECT id FROM KATEGORI_TR_MYPAY WHERE nama = 'Withdraw'))
        RETURNING *
        """,
        [uuid.uuid4(), curr_user["id"], nominal],
    )

    if not withdrawal:
        messages.error(request, "gagal mencatat penarikan")
        return redirect("transaksi:mypay_transaksi")

    # Update balance
    updated_user = db.query_one(
        """
        UPDATE PENGGUNA
        SET saldomypay = saldomypay - %s
        WHERE id = %s
        RETURNING *
        """,
        [nominal, curr_user["id"]],
    )

    if not updated_user:
        messages.error(request, "gagal melakukan penarikan")
        return redirect("transaksi:mypay_transaksi")

    return redirect("transaksi:mypay")
