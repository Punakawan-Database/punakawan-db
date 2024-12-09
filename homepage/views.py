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

# print(categories)
def homepage(request, kategori = None, subkategori = None):
    global categories
    # user = get_user(request)
    userID = request.session.get('user_id')
    # print(userID + " FFF")
    
    selected_category = None
    if (kategori != None and subkategori != None):
        # print(f"ANJAA{kategori}YYYYY")
        fetch_categories2 = db.query_all(f"SELECT * FROM kategori_jasa where id = '{kategori}'")
        
        for j in fetch_categories2:
            j.update({'subcategories': []})

        # print(fetch_categories2)
        for j in fetch_categories2:
            for i in fetch_sub_categories:
                # print(i["kategorijasaid"], j['id'], " FFFFF")
                if (i["kategorijasaid"] == j['id']):
                    # print(subkategori, i['namasubkategori'].lower())
                    if (subkategori in i['namasubkategori'].lower()):
                        j['subcategories'].append(i)
                        
        selected_category = fetch_categories2
        
    elif (kategori != None):
        fetch_categories3 = db.query_all(f"SELECT * FROM kategori_jasa where id = '{kategori}'")
        
        for j in fetch_categories3:
            j.update({'subcategories': []})

        # print(fetch_categories2)
        for j in fetch_categories3:
            for i in fetch_sub_categories:
                # print(i["kategorijasaid"], j['id'], " FFFFF")
                if (i["kategorijasaid"] == j['id']):
                    # print(subkategori, i['namasubkategori'].lower())
                    # if (subkategori in i['namasubkategori'].lower()):
                    j['subcategories'].append(i)
                    
        selected_category = fetch_categories3
    else:
        selected_category = fetch_categories
    
    isPelanggan = False
    for x in pelanggan:
        if str(x['id']) == userID:
            isPelanggan = True
    
    # print(isPelanggan)
    # print(categories)
    context = {
        'isPelanggan' : isPelanggan,
        'title' : 'Trust in Punakawan, because we dont trust ourselves',
        'categories': categories,
        'selected_category': selected_category,
    }
    
    return render(request, 'homepage.html', context)


def subkategori_jasa(request, kategori_slug, subkategori_slug, filtering=None):
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
    
    # print(selected_subcategory)x
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
    voucher_check = db.query_all(f"select * from tr_pembelian_voucher where idpelanggan='{request.session.get('user_id')}' and tglakhir >= current_date")
    # print(voucher_check)
    promo_check = db.query_all(f"select * from promo where tglakhirberlaku >= current_date")
    
    vc = []
    vc2 = []
    
    for x in voucher_check:
        vc.append(x['idvoucher'])
        vc2.append(str(x['idmetodebayar']))
    
    # print(vc)
    # print(vc2)
    
    p = []
    for x in promo_check:
        p.append(x['kode'])
        
    context = {
        'selected_category': selected_category[0],
        'selected_subcategory': selected_subcategory,
        'service_sessions': service_sessions,
        # 'pengguna_testi' : pengguna_testi,
        'workers': workers_lengkap,
        'testimonials' : selected_testimoni,
        'metode_bayar' : metode_bayar,
        'discount_be' : dumps(discID_key),
        'vc' : dumps(vc),
        'vc2' : dumps(vc2),
        'promo' : dumps(p),
        # 'voucher_check' : dumps(voucher_check),
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

def view_pemesanan(request, subkategori=None, status=None):
    bak_id_id = []
    s_pemesanan = db.query_all("SELECT DISTINCT  id FROM tr_pemesanan_jasa")
    for jj in s_pemesanan:
        bak_id_id.append(jj['id'])
    # print(bak_id_id)
    
    orders_bak = db.query_all("""
                            select * from tr_pemesanan_jasa left join testimoni on tr_pemesanan_jasa.id = testimoni.idtrpemesanan, tr_pemesanan_status, status_pesanan where tr_pemesanan_status.idtrpemesanan = tr_pemesanan_jasa.id and tr_pemesanan_status.idstatus = status_pesanan.id;
                            """)
    
    orders_bak2 = db.query_all("""
                            select tr_pemesanan_status.idtrpemesanan, sesi, totalbiaya, string_agg(status, ', '), idpekerja, idkategorijasa, idpelanggan from tr_pemesanan_jasa left join testimoni on tr_pemesanan_jasa.id = testimoni.idtrpemesanan, tr_pemesanan_status, status_pesanan where tr_pemesanan_status.idtrpemesanan = tr_pemesanan_jasa.id and tr_pemesanan_status.idstatus = status_pesanan.id
                            group by tr_pemesanan_status.idtrpemesanan, sesi, totalbiaya, idpekerja, idkategorijasa, idpelanggan;
                            """)
    
    selected_pemesanan = []
    for j in orders_bak2:
        # print(j)
        bak_status = j['string_agg'].split(", ")
        # print("FF ", bak_status, 'Pesanan Dibatalkan' in bak_status, j['idtrpemesanan'])
        if ('Pesanan Dibatalkan' in bak_status):
            j['status'] = 'Pesanan Dibatalkan'
            selected_pemesanan.append(j)
        else:
            if len(bak_status) == 1:
                j['status'] = 'Menunggu Pembayaran'
            if len(bak_status) == 2:
                j['status'] = 'Mencari Pekerja Terdekat'
            if len(bak_status) == 3:
                j['status'] = 'Menunggu Pekerja Berangkat'
            if len(bak_status) == 4:
                j['status'] = 'Pekerja Tiba di Lokasi'
            if len(bak_status) == 5:
                j['status'] = 'Pelayanan Jasa Sedang Dilakukan'
            if len(bak_status) == 6:
                j['status'] = 'Pesanan Selesai'
        
            selected_pemesanan.append(j)
    
    # print(selected_pemesanan)
    # for j in orders_bak:
    #     for i in bak_id_id:
    #         if str(j['idtrpemesanan']) == str(i):
    #             # print("TRUE BOS")
    #             # if (j not in selected_pemesanan):
    #             #     selected_pemesanan.append(j)
    #             appended = False
    #             for k in selected_pemesanan:
    #                 appended = True
    #                 # print(j['idtrpemesanan'], k['idtrpemesanan'])
    #                 print(j['idtrpemesanan'], k['idtrpemesanan'])
    #                 if k['idtrpemesanan'] == j['idtrpemesanan']:
    #                     selected_pemesanan.remove(k)
    #                     selected_pemesanan.append(j)
    #                     break
    #             if (appended == False):
    #                 selected_pemesanan.append(j)
                    
    #             print(appended)
                    
    # print(selected_pemesanan)
    # print("FFF")
                
    # print(orders_bak)
    # print(pengguna)
    for j in selected_pemesanan:
        for i in pengguna:
            if str(j['idpekerja']) == str(i['id']):
                j['worker'] = i['nama']
                
    for j in selected_pemesanan:
        for i in fetch_sub_categories:
            if str(j['idkategorijasa']) == str(i['id']):
                j['subcategory'] = i['namasubkategori']
                
    for j in selected_pemesanan:
        for i in pengguna:
            if str(j['idpelanggan']) == str(i['id']):
                j['customer'] = i['nama']
                
    # print(orders_bak[0])

    order_selector = []
    for i in orders_bak2:
        if str(i['idpelanggan']) == str(request.session.get('user_id')):
            order_selector.append(i)
        
    orders = order_selector
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
    
    selected_subcategories = set()
    selected_statusses = set()
    
    # print(request.session.get('user_id'))
    if (subkategori == None and status == None):
        for xx in orders:
            selected_statusses.add(xx['status'])
            selected_subcategories.add(xx['subcategory'])
            # print(f"FFF {request.session.get('user_id')} {xx['idpelanggan']}")
            if str(xx['idpelanggan']) == str(request.session.get('user_id')):
                selected_orders.append(xx)
                
    elif (subkategori != None and status == None):
        for xx in orders:
            selected_statusses.add(xx['status'])
            selected_subcategories.add(xx['subcategory'])
            # print(f"FFF {request.session.get('user_id')} {xx['idpelanggan']}")
            if str(xx['idpelanggan']) == str(request.session.get('user_id')):
                if (str(xx['subcategory']) == str(subkategori)):
                    selected_orders.append(xx)
                    
                    
    else:
        for xx in orders:
            selected_statusses.add(xx['status'])
            selected_subcategories.add(xx['subcategory'])
            # print(f"FFF {request.session.get('user_id')} {xx['idpelanggan']}")
            if str(xx['idpelanggan']) == str(request.session.get('user_id')):
                if (str(xx['subcategory']) == str(subkategori)):
                    if (str(xx['status']) == str(status)):
                        selected_orders.append(xx)
                        
    # print(selected_orders)
            
    context = {
        'title' : 'Pemesanan',
        's_orders': selected_orders,
        'orders': orders,
        'subcategories': selected_subcategories,
        'statusses': selected_statusses,
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
    timestamp = timestamp.replace(tzinfo=None)
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
    
def batalkan(request, idPesanan) :
    db.query_one(f"insert into tr_pemesanan_status values('{idPesanan}', '{'cdd30b67-9bf9-4999-a46f-ecd23d288058'}', '{datetime.now().replace(tzinfo=None)}')")
        
    return redirect('view_pemesanan')