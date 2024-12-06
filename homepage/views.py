from django.shortcuts import render
from django.urls import *
from utils import db;

# Create your views here.

fetch_categories = db.query_all("SELECT * FROM kategori_jasa")
fetch_sub_categories = db.query_all("SELECT * FROM subkategori_jasa")
pelanggan = db.query_all("SELECT * FROM PELANGGAN")
pekerja = db.query_all("SELECT * FROM PEKERJA")
pengguna = db.query_all("SELECT * from PENGGUNA")

# print(fetch_categories[0]['id'])
# print(fetch_sub_categories[0]['kategorijasaid'])

for j in fetch_categories:
    j.update({'subcategories': []})

# print(fetch_categories)
for j in fetch_categories:
    for i in fetch_sub_categories:
        if (i["kategorijasaid"] == j['id']):
            j['subcategories'].append(i)
            

categories = fetch_categories



testimoni = db.query_all("SELECT * FROM TESTIMONI, tr_pemesanan_jasa where tr_pemesanan_jasa.id = testimoni.idtrpemesanan")
# print(testimoni[0])

def homepage(request):
    context = {
        'title' : 'Trust in Punakawan, because we dont trust ourselves',
        'categories': categories,
    }
    
    return render(request, 'homepage.html', context)


def subkategori_jasa(request, kategori_slug, subkategori_slug):
    selected_category = []
    for x in categories:
        if str(x["id"]) == str(kategori_slug):
            selected_category.append(x)
            break
    
    # print(selected_category)
            
    selected_subcategory = None
    for x in selected_category[0]["subcategories"]:
        if str(x["id"]) == str(subkategori_slug):
            selected_subcategory = x
    
    # print(selected_subcategory)
    # print(type(selected_category[0]))
    # print(temp)
    # print(type(selected_subcategory['id']))
    get_sesi_layanan = db.query_all("select * from sesi_layanan")
    # print(type(get_sesi_layanan))
    
    service_sessions = []
    for x in get_sesi_layanan:
        if x["subkategoriid"] == selected_subcategory['id']:
            service_sessions.append(x)
    
    # print(service_sessions)
    # print(db.query_all(f"SELECT * FROM sesi_layanan where subkategoriid={str(selected_subcategory['id'])}"))
    
    pekerja = db.query_all(f"SELECT * FROM PEKERJA_KATEGORI_JASA")
    # print("FF "+kategori_slug)
    # print(type(pekerja[0]))
    workers_data = []
    for x in pekerja:
    #     print(str(x['kategorijasaid']))
        if str(x['kategorijasaid']) == kategori_slug:
            workers_data.append(x)
        #     # if kategori_slug = 
    # print(workers)
    
    temp_worker = db.query_all("SELECT * FROM PEKERJA")
    # print(temp_worker)
    
    workers = []
    for x in temp_worker:
        for i in workers_data:
            if str(x['id']) == str(i['pekerjaid']):
                workers.append(x)
                
    # print(workers)
    
    get_user = db.query_all("SELECT * FROM PENGGUNA, PEKERJA as pk where PENGGUNA.id = pk.id")
    # print(len(get_user))
    
    # print((workers))
    workers_lengkap = []
    for x in get_user:
        for j in workers:
            if str(x['id']) == str(j['id']):
                workers_lengkap.append(x)
                # print(x['id'], j['id'], j['id']==x['id'])
                
        
    # print(workers_lengkap)
    
    # print(selected_category)
    
    selected_testimoni = []
    for x in testimoni:
        if str(x['idkategorijasa']) == str(subkategori_slug):
            selected_testimoni.append(x)
    
    # print(selected_testimoni)
    for j in pengguna:
        for x in selected_testimoni:
            if (str(x['idpelanggan'])) == str(j['id']):
                x['nama_pelanggan'] = str(j['nama'])
                
    for j in pengguna:
        for x in selected_testimoni:
            if (str(x['idpekerja'])) == str(j['id']):
                x['worker_name'] = str(j['nama'])
                
                
                
    metode_bayar = db.query_all("select * from metode_bayar")
    # print(metode_bayar)
    
    discID = db.query_all("select * from diskon")
    context = {
        'selected_category': selected_category[0],
        'selected_subcategory': selected_subcategory,
        'service_sessions': service_sessions,
        # 'pengguna_testi' : pengguna_testi,
        'workers': workers_lengkap,
        'testimonials' : selected_testimoni,
        'metode_bayar' : metode_bayar,
        'discount_be' : discID,
    }
    
    return render(request, "subkategori.html", context= context)


def subkategori_jasa_pekerja(request, kategori_slug, subkategori_slug):
    selected_category = []
    for x in categories:
        if str(x["id"]) == str(kategori_slug):
            selected_category.append(x)
            break
        
    selected_subcategory = None
    for x in selected_category[0]["subcategories"]:
        if str(x["id"]) == str(subkategori_slug):
            selected_subcategory = x
    
    get_sesi_layanan = db.query_all("select * from sesi_layanan")
    # print(type(get_sesi_layanan))
    
    service_sessions = []
    for x in get_sesi_layanan:
        if x["subkategoriid"] == selected_subcategory['id']:
            service_sessions.append(x)
    
    pekerja = db.query_all(f"SELECT * FROM PEKERJA_KATEGORI_JASA")
    # print("FF "+kategori_slug)
    # print(type(pekerja[0]))
    workers_data = []
    for x in pekerja:
    #     print(str(x['kategorijasaid']))
        if str(x['kategorijasaid']) == kategori_slug:
            workers_data.append(x)
        #     # if kategori_slug = 
    # print(workers)
    
    temp_worker = db.query_all("SELECT * FROM PEKERJA")
    # print(temp_worker)
    
    workers = []
    for x in temp_worker:
        for i in workers_data:
            if str(x['id']) == str(i['pekerjaid']):
                workers.append(x)
                
    # print(workers)
    
    get_user = db.query_all("SELECT * FROM PENGGUNA, PEKERJA as pk where PENGGUNA.id = pk.id")
    # print(len(get_user))
    
    # print((workers))
    workers_lengkap = []
    for x in get_user:
        for j in workers:
            if str(x['id']) == str(j['id']):
                workers_lengkap.append(x)
    
    
    selected_testimoni = []
    for x in testimoni:
        if str(x['idkategorijasa']) == str(subkategori_slug):
            selected_testimoni.append(x)
    
    # print(selected_testimoni)
    for j in pengguna:
        for x in selected_testimoni:
            if (str(x['idpelanggan'])) == str(j['id']):
                x['nama_pelanggan'] = str(j['nama'])
                
    for j in pengguna:
        for x in selected_testimoni:
            if (str(x['idpekerja'])) == str(j['id']):
                x['worker_name'] = str(j['nama'])

    # print(selected_testimoni)
    context = {
        'selected_category': selected_category[0],
        'selected_subcategory': selected_subcategory,
        'service_sessions': service_sessions,
        'workers': workers_lengkap,
        'testimonials': selected_testimoni
    }
    
    return render(request, 'subkategori_pekerja.html', context)

orders = [
        {
            'id': 1,
            'subcategory': 'House Cleaning',
            'service_session': 'Basic Cleaning (2 hours)',
            'total_payment': '150000',
            'worker': 'John Doe',
            'status': 'waiting_payment',
            'has_testimonial': False,
            'get_status_display': 'Menunggu Pembayaran'
        },
        {
            'id': 2,
            'subcategory': 'House Cleaning',
            'service_session': 'Deep Cleaning (4 hours)',
            'total_payment': '300000',
            'worker': None,
            'status': 'finding_worker',
            'has_testimonial': False,
            'get_status_display': 'Mencari Pekerja Terdekat'
        },
        {
            'id': 3,
            'subcategory': 'House Cleaning',
            'service_session': 'Premium Cleaning (6 hours)',
            'total_payment': '450000',
            'worker': 'Jane Smith',
            'status': 'completed',
            'has_testimonial': False,
            'get_status_display': 'Pesanan Selesai'
        },
        {
            'id': 4,
            'subcategory': 'House Cleaning',
            'service_session': 'Basic Cleaning (2 hours)',
            'total_payment': '150000',
            'worker': 'Bob Johnson',
            'status': 'completed',
            'has_testimonial': True,
            'get_status_display': 'Pesanan Selesai'
        }
    ]

order = db.query_all("select * from tr_pemesanan_status, tr_pemesanan_jasa, pekerja, pelanggan status_pesanan where tr_pemesanan_status.idtrpemesanan = tr_pemesanan_jasa.id and tr_pemesanan_status.idstatus = status_pesanan.id and tr_pemesanan_jasa.idpelanggan=pelanggan.id and tr_pemesanan_jasa.idpekerja=pekerja.id")
print(len(order) == len(db.query_all("select * from tr_pemesanan_status")))

def view_pemesanan(request):
    subcategories = []

    for order in orders:
        if order['subcategory'] not in subcategories:
            subcategories.append(order['subcategory'])

    statusses = []

    for order in orders:
        if order['get_status_display'] not in statusses:
            statusses.append(order['get_status_display'])

    context = {
        'title' : 'Pemesanan',
        'orders': orders,
        'subcategories': subcategories,
        'statusses': statusses,
        }
    
    return render(request, 'pemesanan_jasa.html', context)