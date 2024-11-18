from django.shortcuts import render


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
    return render(request, "pekerjaan_jasa.html", context)


def pekerjaan_jasa_status(request):
    return render(request, "pekerjaan_jasa_status.html")
