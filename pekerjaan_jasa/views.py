from django.shortcuts import render

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


# TODO: Add Search Filter Form
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
            tpj.tglpemesanan AS tanggal_pemesanan,
            tpj.tglpekerjaan AS tanggal_pekerjaan,
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


def pekerjaan_jasa_status(request):
    context = {
        "pesanan": [
            {
                "subkategori": "Setrika",
                "nama_pelanggan": "Jono Dewoto",
                "tanggal_pemesanan": "19-10-2020",
                "tanggal_pekerjaan": "19-10-2023",
                "total_biaya": 10000,
                "status_pesanan": "Menunggu Pekerja Berangkat",
            },
            {
                "subkategori": "Daily Cleaning",
                "nama_pelanggan": "Sadewa Wanala",
                "tanggal_pemesanan": "19-10-2020",
                "tanggal_pekerjaan": "19-10-2023",
                "total_biaya": 10000,
                "status_pesanan": "Pekerja Tiba di Lokasi",
            },
            {
                "subkategori": "Pembersihan dapur dan kulkas",
                "nama_pelanggan": "Kuncoro",
                "tanggal_pemesanan": "19-10-2020",
                "tanggal_pekerjaan": "19-10-2023",
                "total_biaya": 10000,
                "status_pesanan": "Pemesanan Jasa Sedang Dilakukan",
            },
            {
                "subkategori": "Kombo daily cleaning + setrika",
                "nama_pelanggan": "Budi Santoso",
                "tanggal_pemesanan": "20-10-2020",
                "tanggal_pekerjaan": "20-10-2023",
                "total_biaya": 15000,
                "status_pesanan": "Pelayanan Selesai",
            },
            {
                "subkategori": "Kombo daily cleaning + dapur",
                "nama_pelanggan": "Siti Aminah",
                "tanggal_pemesanan": "21-10-2020",
                "tanggal_pekerjaan": "21-10-2023",
                "total_biaya": 20000,
                "status_pesanan": "Pesanan Dibatalkan",
            },
            {
                "subkategori": "Daily Cleaning",
                "nama_pelanggan": "Agus Salim",
                "tanggal_pemesanan": "22-10-2020",
                "tanggal_pekerjaan": "22-10-2023",
                "total_biaya": 12000,
                "status_pesanan": "Menunggu Pekerja Berangkat",
            },
            {
                "subkategori": "Cuci Tirai",
                "nama_pelanggan": "Rina Sari",
                "tanggal_pemesanan": "23-10-2020",
                "tanggal_pekerjaan": "23-10-2023",
                "total_biaya": 18000,
                "status_pesanan": "Pekerja Tiba di Lokasi",
            },
            {
                "subkategori": "Cuci Karpet",
                "nama_pelanggan": "Dewi Lestari",
                "tanggal_pemesanan": "24-10-2020",
                "tanggal_pekerjaan": "24-10-2023",
                "total_biaya": 25000,
                "status_pesanan": "Pemesanan Jasa Sedang Dilakukan",
            },
            {
                "subkategori": "Bersih kamar mandi",
                "nama_pelanggan": "Adi Putra",
                "tanggal_pemesanan": "25-10-2020",
                "tanggal_pekerjaan": "25-10-2023",
                "total_biaya": 30000,
                "status_pesanan": "Pelayanan Selesai",
            },
            {
                "subkategori": "Cuci Kasur",
                "nama_pelanggan": "Rudi Hartono",
                "tanggal_pemesanan": "26-10-2020",
                "tanggal_pekerjaan": "26-10-2023",
                "total_biaya": 35000,
                "status_pesanan": "Pesanan Dibatalkan",
            },
            {
                "subkategori": "Cuci Sofa",
                "nama_pelanggan": "Tina Sari",
                "tanggal_pemesanan": "27-10-2020",
                "tanggal_pekerjaan": "27-10-2023",
                "total_biaya": 40000,
                "status_pesanan": "Menunggu Pekerja Berangkat",
            },
            {
                "subkategori": "Setrika",
                "nama_pelanggan": "Bambang Sutrisno",
                "tanggal_pemesanan": "28-10-2020",
                "tanggal_pekerjaan": "28-10-2023",
                "total_biaya": 45000,
                "status_pesanan": "Pekerja Tiba di Lokasi",
            },
            {
                "subkategori": "Pembersihan dapur dan kulkas",
                "nama_pelanggan": "Sari Dewi",
                "tanggal_pemesanan": "29-10-2020",
                "tanggal_pekerjaan": "29-10-2023",
                "total_biaya": 50000,
                "status_pesanan": "Pemesanan Jasa Sedang Dilakukan",
            },
            {
                "subkategori": "Kombo daily cleaning + setrika",
                "nama_pelanggan": "Doni Prasetyo",
                "tanggal_pemesanan": "30-10-2020",
                "tanggal_pekerjaan": "30-10-2023",
                "total_biaya": 55000,
                "status_pesanan": "Pelayanan Selesai",
            },
            {
                "subkategori": "Kombo daily cleaning + dapur",
                "nama_pelanggan": "Lina Marlina",
                "tanggal_pemesanan": "31-10-2020",
                "tanggal_pekerjaan": "31-10-2023",
                "total_biaya": 60000,
                "status_pesanan": "Pesanan Dibatalkan",
            },
        ]
    }
    return render(request, "pekerjaan_jasa_status.html", context)
