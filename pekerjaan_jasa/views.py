from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from utils import db

logged_user = {
    "id": "65ae2c07-9011-4a53-bd88-73a6b577691d",
    "role": "pekerja",
    "nama": "Jhon Doe",
}

# context = {
#     "pesanan": [
#         {
#             "subkategori": "Daily Cleaning",
#             "pelanggan": "Ahmad Fauzi",
#             "tanggal_pemesanan": "19-10-2020",
#             "tanggal_pekerjaan": "19-10-2023",
#             "total_biaya": 10000,
#         },
#     ],
# }

# context = {
#     "pesanan": [
#         {
#             "subkategori": "Setrika",
#             "nama_pelanggan": "Jono Dewoto",
#             "tanggal_pemesanan": "19-10-2020",
#             "tanggal_pekerjaan": "19-10-2023",
#             "total_biaya": 10000,
#             "status_pesanan": "Menunggu Pekerja Berangkat",
#         },
#     ]
# }


def pekerjaan_jasa(request):
    curr_user = logged_user
    # curr_user = request.session.get("user")

    category_filter = request.GET.get("kategori")
    subcategory_filter = request.GET.get("subkategori")

    category_results = db.query_all(
        """
        SELECT
            kj.id AS id_kategori,
            kj.namakategori AS nama_kategori,
            skj.id AS id_subkategori,
            skj.namasubkategori AS nama_subkategori
        FROM PEKERJA pk
            JOIN PEKERJA_KATEGORI_JASA pkj
                ON pkj.pekerjaid = pk.id
            JOIN KATEGORI_JASA kj
                ON kj.id = pkj.kategorijasaid
            JOIN SUBKATEGORI_JASA skj
                ON skj.kategorijasaid = kj.id
        WHERE pk.id = %s
        """,
        [curr_user["id"]],
    )

    orders_statement = """
        SELECT
            skj.namasubkategori AS subkategori,
            ppl.nama AS nama_pelanggan,
            tpj.id AS id_transaksi,
            tpj.tglpemesanan AS tanggal_pemesanan,
            tpj.sesi AS sesi,
            tpj.totalbiaya AS total_biaya
        FROM TR_PEMESANAN_JASA tpj
            JOIN PELANGGAN pl
                ON pl.id = tpj.idpelanggan
            JOIN PENGGUNA ppl
                ON ppl.id = pl.id
            JOIN SESI_LAYANAN sl
                ON sl.subkategoriid = tpj.idkategorijasa
                AND sl.sesi = tpj.sesi
            JOIN SUBKATEGORI_JASA skj
                ON skj.id = sl.subkategoriid
            JOIN KATEGORI_JASA kj
                ON kj.id = skj.kategorijasaid
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
            sp.status = 'Mencari Pekerja Terdekat'
            AND skj.id IN (
                SELECT
                    skj.id
                FROM PEKERJA pk
                    JOIN PEKERJA_KATEGORI_JASA pkj
                        ON pkj.pekerjaid = pk.id
                    JOIN KATEGORI_JASA kj
                        ON kj.id = pkj.kategorijasaid
                    JOIN SUBKATEGORI_JASA skj
                        ON skj.kategorijasaid = kj.id
                WHERE pk.id = %s
            )
    """

    orders_params = [curr_user["id"]]
    orders_conditions = []

    if category_filter:
        orders_conditions.append("kj.id = %s")
        orders_params.append(category_filter)

    if subcategory_filter:
        orders_conditions.append("skj.id = %s")
        orders_params.append(subcategory_filter)

    if orders_conditions:
        orders_statement += " AND " + " AND ".join(orders_conditions)

    order_results = db.query_all(orders_statement, orders_params)

    context = {
        "kategori": [
            {"id_kategori": id_kategori, "nama_kategori": nama_kategori}
            for id_kategori, nama_kategori in set(
                (res["id_kategori"], res["nama_kategori"]) for res in category_results
            )
        ],
        "subkategori": category_results,
        "pesanan": order_results,
    }

    return render(request, "pekerjaan_jasa.html", context)


@require_POST
# TODO: Better error handling
def pekerjaan_jasa_update(request):
    curr_user = logged_user
    # curr_user = request.session.get("user")

    order_id = request.POST.get("order_id")
    if not order_id:
        return HttpResponseBadRequest("order_id kosong")

    status_result = db.query_one(
        """
        SELECT sp.id FROM STATUS_PESANAN sp
        WHERE sp.status = 'Menunggu Pekerja Berangkat'
        """
    )

    if not status_result:
        return HttpResponseServerError("status 'Menunggu Pekerja Berangkat' tidak ditemukan")

    updated_order = db.query_one(
        """
        INSERT INTO TR_PEMESANAN_STATUS
        (idtrpemesanan, idstatus, tglwaktu)
        VALUES (%s, %s, NOW())
        RETURNING *
        """,
        [order_id, status_result["id"]],
    )

    updated_transaksi = db.query_one(
        """
        UPDATE TR_PEMESANAN_JASA
        SET idpekerja = %s,
            tglpekerjaan = CURRENT_DATE,
            waktupekerjaan = CURRENT_DATE + interval '1 day' * sesi
        WHERE id_tr_pemesanan_jasa = %s
        """,
        [curr_user["id"], order_id],
    )

    if updated_order and updated_transaksi:
        messages.success(request, "status pesanan berhasil diperbarui")
    else:
        messages.error(request, "gagal memperbarui status pesanan")

    return redirect("pekerjaan_jasa:pekerjaan_jasa")


def pekerjaan_jasa_status(request):
    curr_user = logged_user
    # curr_user = request.session.get("user")

    subcategory_filter = request.GET.get("subkategori")
    status_filter = request.GET.get("status")

    # FIXME: Refactor this, if u can remove this
    status_results = db.query_all(
        """
        SELECT
            sp.id AS id_status,
            sp.status AS nama_status
        FROM STATUS_PESANAN sp
        WHERE sp.status IN (
            'Menunggu Pekerja Berangkat',
            'Pekerja Tiba di Lokasi',
            'Pelayanan Jasa Sedang Dilakukan',
            'Pesanan Selesai',
            'Pesanan Dibatalkan'
        )
        """
    )

    orders_statement = """
        SELECT
            skj.namasubkategori AS subkategori,
            ppl.nama AS nama_pelanggan,
            tpj.id AS id_transaksi,
            tpj.tglpemesanan AS tanggal_pemesanan,
            tpj.sesi AS sesi,
            tpj.totalbiaya AS total_biaya,
            sp.status AS status_pesanan,
            CASE sp.status
                WHEN 'Menunggu Pekerja Berangkat' THEN (
                    SELECT id FROM STATUS_PESANAN WHERE status = 'Pekerja Tiba di Lokasi'
                )
                WHEN 'Pekerja Tiba di Lokasi' THEN (
                    SELECT id FROM STATUS_PESANAN WHERE status = 'Pelayanan Jasa Sedang Dilakukan'
                )
                WHEN 'Pelayanan Jasa Sedang Dilakukan' THEN (
                    SELECT id FROM STATUS_PESANAN WHERE status = 'Pesanan Selesai'
                )
                WHEN 'Pesanan Selesai' THEN NULL
                WHEN 'Pesanan Dibatalkan' THEN NULL
            END AS next_status_id,
            CASE sp.status
                WHEN 'Menunggu Pekerja Berangkat' THEN 'Pekerja Tiba di Lokasi'
                WHEN 'Pekerja Tiba di Lokasi' THEN 'Pelayanan Jasa Sedang Dilakukan'
                WHEN 'Pelayanan Jasa Sedang Dilakukan' THEN 'Pesanan Selesai'
                WHEN 'Pesanan Selesai' THEN NULL
                WHEN 'Pesanan Dibatalkan' THEN NULL
            END AS next_status_pesanan
        FROM TR_PEMESANAN_JASA tpj
            JOIN PELANGGAN pl
                ON pl.id = tpj.idpelanggan
            JOIN PENGGUNA ppl
                ON ppl.id = pl.id
            JOIN PEKERJA pk
                ON pk.id = tpj.idpekerja
            JOIN SESI_LAYANAN sl
                ON sl.subkategoriid = tpj.idkategorijasa
                AND sl.sesi = tpj.sesi
            JOIN SUBKATEGORI_JASA skj
                ON skj.id = sl.subkategoriid
            JOIN KATEGORI_JASA kj
                ON kj.id = skj.kategorijasaid
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
            sp.status IN (
                'Menunggu Pekerja Berangkat',
                'Pekerja Tiba di Lokasi',
                'Pelayanan Jasa Sedang Dilakukan',
                'Pesanan Selesai',
                'Pesanan Dibatalkan'
            )
            AND pk.id = %s
    """

    orders_params = [curr_user["id"]]
    orders_conditions = []

    if subcategory_filter:
        orders_conditions.append("skj.namasubkategori ILIKE %s")
        orders_params.append(f"%{subcategory_filter}%")

    if status_filter:
        orders_conditions.append("sp.id = %s")
        orders_params.append(status_filter)

    if orders_conditions:
        orders_statement += " AND " + " AND ".join(orders_conditions)

    order_results = db.query_all(orders_statement, orders_params)

    context = {
        "status": status_results,
        "pesanan": order_results,
    }

    return render(request, "pekerjaan_jasa_status.html", context)


@require_POST
# TODO: Better error handling
def pekerjaan_jasa_status_update(request):
    order_id = request.POST.get("order_id")
    status_id = request.POST.get("status_id")

    if not order_id or not status_id:
        return HttpResponseBadRequest("data request tidak lengkap")

    updated_order = db.query_one(
        """
        INSERT INTO TR_PEMESANAN_STATUS
        (idtrpemesanan, idstatus, tglwaktu)
        VALUES (%s, %s, NOW())
        RETURNING *
        """,
        [order_id, status_id],
    )

    if updated_order:
        messages.success(request, "status pesanan berhasil diperbarui")
    else:
        messages.error(request, "gagal memperbarui status pesanan")

    return redirect("pekerjaan_jasa:pekerjaan_jasa_status")
