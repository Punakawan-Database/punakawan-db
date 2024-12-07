import datetime
import uuid
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

def register(request):
    return render(request, 'register.html')
  
def register_pelanggan(request):
    if request.method == "POST":
        try:
            # GET data dari form
            nama = request.POST.get('name')
            password = request.POST.get('password')
            jeniskelamin = request.POST.get('gender')
            nohp = request.POST.get('phone')
            tgllahir = parse_date(request.POST.get('dob'))  # parse date
            alamat = request.POST.get('address')
            
            # cek apakah nohp sudah teregister sebelumnya
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM pengguna WHERE nohp = %s", [nohp])
                if cursor.fetchone()[0] > 0:
                    messages.error(request, "Nomor handphone sudah terdaftar. Gunakan nomor lain.")
                    return redirect('register_pelanggan') 

            # generate UUID
            user_id = str(uuid.uuid4())

            # insert data ke tabel `pengguna` 
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pengguna (id, nama, jeniskelamin, nohp, pwd, tgllahir, alamat, saldomypay)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [user_id, nama, jeniskelamin, nohp, password, tgllahir, alamat, 0])

            # insert data ke tabel `pelanggan`
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pelanggan (id, level)
                    VALUES (%s, %s)
                """, [user_id, "Bronze"])

            return redirect('login')  

        # error handling
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('register_pelanggan') 

    return render(request, 'register_pelanggan.html')

def register_pekerja(request):
    if request.method == "POST":
        try:
            # GET data dari form
            nama = request.POST.get('name')
            password = request.POST.get('password')
            jeniskelamin = request.POST.get('gender')
            nohp = request.POST.get('phone')
            tgllahir = parse_date(request.POST.get('dob'))  # parse date
            alamat = request.POST.get('address')
            namabank = request.POST.get('bank')
            nomorrekening = request.POST.get('account')
            npwp = request.POST.get('npwp')
            linkfoto = request.POST.get('photo')

            # validasi input
            if not (nama and password and jeniskelamin and nohp and tgllahir and alamat and namabank and nomorrekening):
                messages.error(request, "Semua field perlu diisi.")
                return redirect('register_pekerja')
            
            # cek apakah nohp sudah teregister sebelumnya
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM pengguna WHERE nohp = %s", [nohp])
                if cursor.fetchone()[0] > 0:
                    messages.error(request, "Nomor handphone sudah terdaftar. Gunakan nomor lain.")
                    return redirect('register_pekerja') 

            # generate UUID
            user_id = str(uuid.uuid4())

            # insert data ke tabel `pengguna`
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pengguna (id, nama, jeniskelamin, nohp, pwd, tgllahir, alamat, saldomypay)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [user_id, nama, jeniskelamin, nohp, password, tgllahir, alamat, 0])

            # insert data ke tabel `pekerja`
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pekerja (id, namabank, nomorrekening, npwp, linkfoto, rating, jmlpesananselesai)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [user_id, namabank, nomorrekening, npwp, linkfoto, 0.0, 0])  # default rating: 0.0, orders: 0

            return redirect('login')  
        
        # error handling
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('register_pekerja') 

    return render(request, 'register_pekerja.html')


def login(request):
    if request.method == 'POST':
        no_hp = request.POST['no_hp']
        password = request.POST['password']

        # query untuk verify id user pada tabel `pengguna`
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nohp FROM pengguna 
                WHERE nohp = %s AND pwd = %s
            """, [no_hp, password])
            user_result = cursor.fetchone()
            print(user_result)

        if user_result:
            request.session['user_id'] = str(user_result[0]) # simpan user id ke session
            # print(request.session['user_id'] + " FF")
            user_id, user_nohp = user_result

            # menentukan role
            with connection.cursor() as cursor:
                # cek jika user 'pelanggan'
                cursor.execute("SELECT EXISTS (SELECT 1 FROM pelanggan WHERE id = %s)", [user_id])
                is_pelanggan = cursor.fetchone()[0]

                if is_pelanggan:
                    request.session['user_role'] = 'pelanggan'  # simpan role ke session
                    response = render(request, 'main_pelanggan.html')
                    response.set_cookie('user_id', user_id)  # set user id cookie
                    return response

                # cek jika user 'pekerja'
                cursor.execute("SELECT EXISTS (SELECT 1 FROM pekerja WHERE id = %s)", [user_id])
                is_pekerja = cursor.fetchone()[0]

                if is_pekerja:
                    request.session['user_role'] = 'pekerja'  # simpan role ke session
                    response = render(request, 'main_pekerja.html')
                    response.set_cookie('user_id', user_id)  # set user id cookie
                    return response

        # error handling
        messages.error(request, 'Invalid credentials.')
        return redirect('login')
    
    return render(request, 'login.html')

def profile_pelanggan(request):
    # GET id dari cookie
    user_id = request.COOKIES.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view your profile.")
        return redirect('login')

    try:
        # fetch user detail dari tabel `pengguna`
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nama, jeniskelamin, nohp, tgllahir, alamat, saldomypay 
                FROM pengguna 
                WHERE id = %s
            """, [user_id])
            user_data = cursor.fetchone()

        if not user_data:
            messages.error(request, "User not found.")
            return redirect('login')

        # unpack 
        nama, jeniskelamin, nohp, tgllahir, alamat, saldomypay = user_data

        # fetch level dari tabel `pelanggan`
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT level 
                FROM pelanggan 
                WHERE id = %s
            """, [user_id])
            level_data = cursor.fetchone()

        level = level_data[0] if level_data else "Unknown"

        # context
        context = {
            'nama': nama,
            'jeniskelamin': "Laki-laki" if jeniskelamin.lower() == 'l' else "Perempuan",
            'nohp': nohp,
            'tgllahir': tgllahir,
            'alamat': alamat,
            'level': level,
            'saldo': saldomypay 
        }

        return render(request, 'profile_pelanggan.html', context)

    # error handling
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('login')

def profile_pekerja(request):
    # GET id dari cookie
    user_id = request.COOKIES.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view your profile.")
        return redirect('login')

    try:
        # fetch user detail dari tabel `pengguna`
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT nama, jeniskelamin, nohp, tgllahir, alamat, saldomypay 
                FROM pengguna 
                WHERE id = %s
            """, [user_id])
            user_data = cursor.fetchone()

        if not user_data:
            messages.error(request, "User not found.")
            return redirect('login')

        # unpack
        nama, jeniskelamin, nohp, tgllahir, alamat, saldomypay = user_data

        # fetch detail pekerja dari tabel `pekerja`
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT namabank, nomorrekening, npwp, linkfoto, rating, jmlpesananselesai
                FROM pekerja
                WHERE id = %s
            """, [user_id])
            pekerja_data = cursor.fetchone()

        if pekerja_data:
            namabank, nomorrekening, npwp, linkfoto, rating, jmlpesananselesai = pekerja_data
        else:
            namabank = nomorrekening = npwp = linkfoto = rating = jmlpesananselesai = None

        # fetch kategori jasa pekerja
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT kj.namakategori
                FROM pekerja_kategori_jasa pkj
                JOIN kategori_jasa kj ON pkj.kategorijasaid = kj.id
                WHERE pkj.pekerjaid = %s
            """, [user_id])
            kategori_jasa = [row[0] for row in cursor.fetchall()]  # List of `namakategori`

        # context
        context = {
            'nama': nama,
            'jeniskelamin': "Laki-laki" if jeniskelamin.lower() == 'l' else "Perempuan",
            'nohp': nohp,
            'tgllahir': tgllahir,
            'alamat': alamat,
            'saldo': saldomypay,
            'namabank': namabank,
            'nomorrekening': nomorrekening,
            'npwp': npwp,
            'linkfoto': linkfoto,
            'rating': rating,
            'jmlpesananselesai': jmlpesananselesai,
            'kategori_jasa': kategori_jasa,
        }

        return render(request, 'profile_pekerja.html', context)

    # error handling
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('login')

def update_pelanggan(request):
    # GET user id dari cookie
    user_id = request.COOKIES.get('user_id')  
    
    if not user_id:
        messages.error(request, "You need to log in to update your profile.")
        return redirect('login')

    if request.method == 'POST':
        # GET data dari form
        full_name = request.POST.get('full_name')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')

        try:
            # update tabel `pengguna` 
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE pengguna
                    SET nama = %s, jeniskelamin = %s, nohp = %s, tgllahir = %s, alamat = %s
                    WHERE id = %s
                """, [full_name, gender, phone_number, date_of_birth, address, user_id])

            return redirect('profile_pelanggan')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('update_pelanggan')

    else:
        try:
            # retrieve data user dari tabel `pengguna` dan `pelanggan`
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.nama, p.jeniskelamin, p.nohp, p.tgllahir, p.alamat, p.saldomypay, pl.level
                    FROM pengguna p
                    JOIN pelanggan pl ON p.id = pl.id
                    WHERE p.id = %s
                """, [user_id])
                user_data = cursor.fetchone()

            if user_data:
                context = {
                    'user': {
                        'full_name': user_data[0],
                        'gender': user_data[1],
                        'phone_number': user_data[2],
                        'date_of_birth': user_data[3],
                        'address': user_data[4],
                        'mypay_balance': user_data[5],
                        'level': user_data[6],
                    }
                }
                return render(request, 'update_pelanggan.html', context)
            else:
                messages.error(request, "User not found.")
                return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('login')


def update_pekerja(request):
    # GET user id dari cookie
    user_id = request.COOKIES.get('user_id')  

    if not user_id:
        messages.error(request, "You need to log in to update your profile.")
        return redirect('login')

    if request.method == 'POST':
        # GET data dari form
        nama = request.POST.get('nama')
        gender = request.POST.get('gender')
        no_hp = request.POST.get('no_hp')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        alamat = request.POST.get('alamat')
        nama_bank = request.POST.get('nama_bank')
        no_rekening = request.POST.get('no_rekening')
        npwp = request.POST.get('npwp')
        url_foto = request.POST.get('url_foto')

        try:
            # update tabel `pengguna`
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE pengguna
                    SET nama = %s, jeniskelamin = %s, nohp = %s, tgllahir = %s, alamat = %s
                    WHERE id = %s
                """, [nama, gender, no_hp, tanggal_lahir, alamat, user_id])

            # update tabel `pekerja`
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE pekerja
                    SET namabank = %s, nomorrekening = %s, npwp = %s, linkfoto = %s
                    WHERE id = %s
                """, [nama_bank, no_rekening, npwp, url_foto, user_id])

            return redirect('profile_pekerja')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('update_pekerja')

    else:
        try:
            # retrieve data pekerja dari `pengguna` dan `pekerja`
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.nama, p.jeniskelamin, p.nohp, p.tgllahir, p.alamat,
                           pk.namabank, pk.nomorrekening, pk.npwp, pk.linkfoto
                    FROM pengguna p
                    JOIN pekerja pk ON p.id = pk.id
                    WHERE p.id = %s
                """, [user_id])
                pekerja_data = cursor.fetchone()

            if pekerja_data:
                context = {
                    'pekerja': {
                        'nama': pekerja_data[0],
                        'gender': pekerja_data[1],
                        'no_hp': pekerja_data[2],
                        'tanggal_lahir': pekerja_data[3],
                        'alamat': pekerja_data[4],
                        'nama_bank': pekerja_data[5],
                        'no_rekening': pekerja_data[6],
                        'npwp': pekerja_data[7],
                        'url_foto': pekerja_data[8],
                    }
                }
                return render(request, 'update_pekerja.html', context)
            else:
                messages.error(request, "Worker not found.")
                return redirect('login')
        
        # error handling
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('login')


def logout_view(request):
    response = redirect('login')
    
    # delete cookie `user_id`
    response.delete_cookie('user_id')
    
    return response