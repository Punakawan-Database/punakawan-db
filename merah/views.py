from django.shortcuts import render


def mypay(request):
    context = {
        "user": {
            "role": "pengguna",
            "nama": "John Doe",
            "no_hp": "085172239073",
            "saldo": 1000000000,
            "riwayat_tansaksi": [
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
        },
    }
    return render(request, "merah/mypay.html", context)


def mypay_transaksi(request):
    context = {
        "user": {
            "role": "pengguna",
            "nama": "John Doe",
            "no_hp": "085172239073",
            "saldo": 1000000000,
        },
    }
    return render(request, "merah/mypay_transaksi.html", context)


def pekerjaan_jasa(request):
    context = {
        "pesanan": [
            {
                "subkategori": "Setrika",
                "nama_pelanggan": "Ahmad Fauzi",
                "tanggal_pemesanan": "19-10-2020",
                "tanggal_pekerjaan": "19-10-2023",
                "total_biaya": 10000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Daily Cleaning",
                "nama_pelanggan": "Budi Hartono",
                "tanggal_pemesanan": "19-10-2020",
                "tanggal_pekerjaan": "19-10-2023",
                "total_biaya": 10000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Dapur",
                "nama_pelanggan": "Citra Dewi",
                "tanggal_pemesanan": "19-10-2020",
                "tanggal_pekerjaan": "19-10-2023",
                "total_biaya": 10000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Cuci Mobil",
                "nama_pelanggan": "Dian Prasetyo",
                "tanggal_pemesanan": "20-10-2020",
                "tanggal_pekerjaan": "20-10-2023",
                "total_biaya": 15000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Kamar",
                "nama_pelanggan": "Eka Sari",
                "tanggal_pemesanan": "21-10-2020",
                "tanggal_pekerjaan": "21-10-2023",
                "total_biaya": 20000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Halaman",
                "nama_pelanggan": "Fajar Nugroho",
                "tanggal_pemesanan": "22-10-2020",
                "tanggal_pekerjaan": "22-10-2023",
                "total_biaya": 12000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Jendela",
                "nama_pelanggan": "Gita Lestari",
                "tanggal_pemesanan": "23-10-2020",
                "tanggal_pekerjaan": "23-10-2023",
                "total_biaya": 18000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Karpet",
                "nama_pelanggan": "Hadi Pranoto",
                "tanggal_pemesanan": "24-10-2020",
                "tanggal_pekerjaan": "24-10-2023",
                "total_biaya": 25000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Kolam",
                "nama_pelanggan": "Indah Permata",
                "tanggal_pemesanan": "25-10-2020",
                "tanggal_pekerjaan": "25-10-2023",
                "total_biaya": 30000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Atap",
                "nama_pelanggan": "Joko Susilo",
                "tanggal_pemesanan": "26-10-2020",
                "tanggal_pekerjaan": "26-10-2023",
                "total_biaya": 35000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Garasi",
                "nama_pelanggan": "Kiki Amalia",
                "tanggal_pemesanan": "27-10-2020",
                "tanggal_pekerjaan": "27-10-2023",
                "total_biaya": 40000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Taman",
                "nama_pelanggan": "Lukman Hakim",
                "tanggal_pemesanan": "28-10-2020",
                "tanggal_pekerjaan": "28-10-2023",
                "total_biaya": 45000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Gudang",
                "nama_pelanggan": "Maya Sari",
                "tanggal_pemesanan": "29-10-2020",
                "tanggal_pekerjaan": "29-10-2023",
                "total_biaya": 50000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Kaca",
                "nama_pelanggan": "Nina Kartika",
                "tanggal_pemesanan": "30-10-2020",
                "tanggal_pekerjaan": "30-10-2023",
                "total_biaya": 55000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
            {
                "subkategori": "Pembersihan Perabot",
                "nama_pelanggan": "Omar Dani",
                "tanggal_pemesanan": "31-10-2020",
                "tanggal_pekerjaan": "31-10-2023",
                "total_biaya": 60000,
                "status_pesanan": "Mencari Pekerja Terdekat",
            },
        ]
    }
    return render(request, "merah/pekerjaan_jasa", context)


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
                "subkategori": "Pembersihan Dapur",
                "nama_pelanggan": "Kuncoro",
                "tanggal_pemesanan": "19-10-2020",
                "tanggal_pekerjaan": "19-10-2023",
                "total_biaya": 10000,
                "status_pesanan": "Pemesanan Jasa Sedang Dilakukan",
            },
            {
                "subkategori": "Cuci Mobil",
                "nama_pelanggan": "Budi Santoso",
                "tanggal_pemesanan": "20-10-2020",
                "tanggal_pekerjaan": "20-10-2023",
                "total_biaya": 15000,
                "status_pesanan": "Pelayanan Selesai",
            },
            {
                "subkategori": "Pembersihan Kamar",
                "nama_pelanggan": "Siti Aminah",
                "tanggal_pemesanan": "21-10-2020",
                "tanggal_pekerjaan": "21-10-2023",
                "total_biaya": 20000,
                "status_pesanan": "Pesanan Dibatalkan",
            },
            {
                "subkategori": "Pembersihan Halaman",
                "nama_pelanggan": "Agus Salim",
                "tanggal_pemesanan": "22-10-2020",
                "tanggal_pekerjaan": "22-10-2023",
                "total_biaya": 12000,
                "status_pesanan": "Menunggu Pekerja Berangkat",
            },
            {
                "subkategori": "Pembersihan Jendela",
                "nama_pelanggan": "Rina Sari",
                "tanggal_pemesanan": "23-10-2020",
                "tanggal_pekerjaan": "23-10-2023",
                "total_biaya": 18000,
                "status_pesanan": "Pekerja Tiba di Lokasi",
            },
            {
                "subkategori": "Pembersihan Karpet",
                "nama_pelanggan": "Dewi Lestari",
                "tanggal_pemesanan": "24-10-2020",
                "tanggal_pekerjaan": "24-10-2023",
                "total_biaya": 25000,
                "status_pesanan": "Pemesanan Jasa Sedang Dilakukan",
            },
            {
                "subkategori": "Pembersihan Kolam",
                "nama_pelanggan": "Adi Putra",
                "tanggal_pemesanan": "25-10-2020",
                "tanggal_pekerjaan": "25-10-2023",
                "total_biaya": 30000,
                "status_pesanan": "Pelayanan Selesai",
            },
            {
                "subkategori": "Pembersihan Atap",
                "nama_pelanggan": "Rudi Hartono",
                "tanggal_pemesanan": "26-10-2020",
                "tanggal_pekerjaan": "26-10-2023",
                "total_biaya": 35000,
                "status_pesanan": "Pesanan Dibatalkan",
            },
            {
                "subkategori": "Pembersihan Garasi",
                "nama_pelanggan": "Tina Sari",
                "tanggal_pemesanan": "27-10-2020",
                "tanggal_pekerjaan": "27-10-2023",
                "total_biaya": 40000,
                "status_pesanan": "Menunggu Pekerja Berangkat",
            },
            {
                "subkategori": "Pembersihan Taman",
                "nama_pelanggan": "Bambang Sutrisno",
                "tanggal_pemesanan": "28-10-2020",
                "tanggal_pekerjaan": "28-10-2023",
                "total_biaya": 45000,
                "status_pesanan": "Pekerja Tiba di Lokasi",
            },
            {
                "subkategori": "Pembersihan Gudang",
                "nama_pelanggan": "Sari Dewi",
                "tanggal_pemesanan": "29-10-2020",
                "tanggal_pekerjaan": "29-10-2023",
                "total_biaya": 50000,
                "status_pesanan": "Pemesanan Jasa Sedang Dilakukan",
            },
            {
                "subkategori": "Pembersihan Kaca",
                "nama_pelanggan": "Doni Prasetyo",
                "tanggal_pemesanan": "30-10-2020",
                "tanggal_pekerjaan": "30-10-2023",
                "total_biaya": 55000,
                "status_pesanan": "Pelayanan Selesai",
            },
            {
                "subkategori": "Pembersihan Perabot",
                "nama_pelanggan": "Lina Marlina",
                "tanggal_pemesanan": "31-10-2020",
                "tanggal_pekerjaan": "31-10-2023",
                "total_biaya": 60000,
                "status_pesanan": "Pesanan Dibatalkan",
            },
        ]
    }
    return render(request, "merah/pekerjaan_jasa", context)
