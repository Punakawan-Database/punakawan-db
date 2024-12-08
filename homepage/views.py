from django.shortcuts import render, redirect
from django.urls import *
from utils import db;

from django.contrib.auth import get_user
from json import dumps 
import requests

from datetime import date, datetime
# from django.contrib.auth.models import UserProfile
# from django.auth.models import UserProfile

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
    # user = get_user(request)
    userID = request.session.get('user_id')
    # print(userID + " FFF")
    
    isPelanggan = False
    for x in pelanggan:
        if str(x['id']) == userID:
            isPelanggan = True
    
    # print(isPelanggan)
    context = {
        'isPelanggan' : isPelanggan,
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
    discID_key = list()
    for x in discID:
        discID_key.append([x['kode'], int(x['potongan'])])
        x['potongan'] = int(x['potongan'])
        
    # print(dumps(discID_key))
    context = {
        'selected_category': selected_category[0],
        'selected_subcategory': selected_subcategory,
        'service_sessions': service_sessions,
        # 'pengguna_testi' : pengguna_testi,
        'workers': workers_lengkap,
        'testimonials' : selected_testimoni,
        'metode_bayar' : metode_bayar,
        'discount_be' : dumps(discID_key),
    }
    
    return render(request, "subkategori.html", context= context)

# def verify_discount(request):
#     print("TT")
#     return "TESTINGGGGGG"
    
    
def subkategori_jasa_pekerja(request, kategori_slug, subkategori_slug):
    userID = request.session.get('user_id')
    print(str(userID) + " userID")
    
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
        'category_slug' : str(kategori_slug),
        'selected_category' : selected_category[0],
        'selected_subcategory': selected_subcategory,
        'service_sessions': service_sessions,
        'workers': workers_lengkap,
        'testimonials': selected_testimoni
    }
    
    return render(request, 'subkategori_pekerja.html', context)


# print(orders)

# order = db.query_all("select * from tr_pemesanan_status, tr_pemesanan_jasa, pekerja, pelanggan status_pesanan where tr_pemesanan_status.idtrpemesanan = tr_pemesanan_jasa.id and tr_pemesanan_status.idstatus = status_pesanan.id and tr_pemesanan_jasa.idpelanggan=pelanggan.id and tr_pemesanan_jasa.idpekerja=pekerja.id")
# print(len(order) == len(db.query_all("select * from tr_pemesanan_status")))

def view_pemesanan(request):
    orders_bak = db.query_all("select * from tr_pemesanan_jasa left join testimoni on tr_pemesanan_jasa.id = testimoni.idtrpemesanan, tr_pemesanan_status, status_pesanan where tr_pemesanan_status.idtrpemesanan = tr_pemesanan_jasa.id and tr_pemesanan_status.idstatus = status_pesanan.id;")
    # print(orders_bak)
    # print(pengguna)
    for j in orders_bak:
        for i in pengguna:
            if str(j['idpekerja']) == str(i['id']):
                j['worker'] = i['nama']
                
    for j in orders_bak:
        for i in fetch_sub_categories:
            if str(j['idkategorijasa']) == str(i['id']):
                j['subcategory'] = i['namasubkategori']
                
    for j in orders_bak:
        for i in pengguna:
            if str(j['idpelanggan']) == str(i['id']):
                j['customer'] = i['nama']
                
    # print(orders_bak[0])

    orders = orders_bak
    
    # print(metode+" FFF")
    # db.query_one(f"INSERT INTO tr_pemesanan_jasa (idpelanggan, idpekerja, idkategorijasa, idmetodebayar, iddiskon, idstatus, tanggal) VALUES ({request.session.get('user_id')}, {'null'}, {request.POST['subkategori']}, {request.POST['metode_bayar']}, {request.POST['diskon']}, 1, '{request.POST['tanggal']}')")
    # subcategories = []

    # for order in orders:
    #     if order['subcategory'] not in subcategories:
    #         subcategories.append(order['subcategory'])

    # statusses = []

    # for order in orders:
    #     if order['get_status_display'] not in statusses:
    #         statusses.append(order['get_status_display'])
    selected_orders = []
    
    # print(request.session.get('user_id'))
    for xx in orders:
        # print(f"FFF {request.session.get('user_id')} {xx['idpelanggan']}")
        if str(xx['idpelanggan']) == str(request.session.get('user_id')):
            selected_orders.append(xx)
            
    print(selected_orders)
            
    context = {
        'title' : 'Pemesanan',
        'orders': selected_orders,
        }
    
    return render(request, 'pemesanan_jasa.html', context)

# def buat_order(request):
#     db.query_one(f"INSERT INTO tr_pemesanan_jasa (idpelanggan, idpekerja, idkategorijasa, idmetodebayar, iddiskon, idstatus, tanggal) VALUES ({request.session.get('user_id')}, {request.POST['pekerja']}, {request.POST['subkategori']}, {request.POST['metode_bayar']}, {request.POST['diskon']}, 1, '{request.POST['tanggal']}')")

def bergabung(request, kategori):
    userID = request.session.get('user_id')
    userID = str(userID)
    
    db.query_one(f"insert into pekerja_kategori_jasa values('{userID}', '{kategori}')")
    # print(kategori)
    
    return redirect('homepage')

def pesan(request, idKategoriJasa, Sesi, idMetodeBayar, price, idDiskon=None):
    userID = request.session.get('user_id')
    userID = str(userID)
    
    uuid_generator = db.query_one("select uuid_generate_v4()")
    uuid_generator = uuid_generator['uuid_generate_v4']
    dates = date.today()
    timestamp = datetime.now()
    if (idDiskon == None):
        # print(uuid_generator['uuid_generate_v4'])
        # print("FFF")
        db.query_one(f"insert into tr_pemesanan_jasa values('{uuid_generator}', '{dates}', null, null, '{price}', '{userID}', null, '{idKategoriJasa}', '{Sesi}', null, '{idMetodeBayar}')")
        db.query_one(f"insert into tr_pemesanan_status values('{uuid_generator}', 'feae3333-a7df-4800-a26e-a0017bbaf59c', '{timestamp}')")
    else:
        db.query_one(f"insert into tr_pemesanan_jasa values('{uuid_generator}', '{dates}', null, null, '{price}', '{userID}', null, '{idKategoriJasa}', '{Sesi}', '{idDiskon}', '{idMetodeBayar}')")
        db.query_one(f"insert into tr_pemesanan_status values('{uuid_generator}', 'feae3333-a7df-4800-a26e-a0017bbaf59c', '{timestamp}')")
    # print(f"{idKategoriJasa} {Sesi} {idMetodeBayar} {idDiskon}")
    
    
    # db.query_one(f"insert into tr_pemesanan_jasa (idpelanggan, idpekerja, idkategorijasa, idmetodebayar, iddiskon, idstatus, tanggal) values('{userID}', null, '{idKategoriJasa}', '{idMetodeBayar}', '{idDiskon}', 1, '2020-12-12')")
    
    return redirect('view_pemesanan')
    # return homepage(request=request)