import datetime
import uuid
from .forms import PenggunaRegistrationForm, PekerjaRegistrationForm, EditProfileForm
from .decorators import role_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.utils.dateparse import parse_date

def register(request):
    return render(request, 'register.html')
  
def register_pelanggan(request):
    if request.method == "POST":
        try:
            # Get data from the form
            nama = request.POST.get('name')
            password = request.POST.get('password')
            jeniskelamin = request.POST.get('gender')
            nohp = request.POST.get('phone')
            tgllahir = parse_date(request.POST.get('dob'))  # Parse the date input
            alamat = request.POST.get('address')

            # Generate a new UUID for the user
            user_id = str(uuid.uuid4())

            # Insert data into the `pengguna` table
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pengguna (id, nama, jeniskelamin, nohp, pwd, tgllahir, alamat, saldomypay)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [user_id, nama, jeniskelamin, nohp, password, tgllahir, alamat, 0])

            # Insert data into the `pelanggan` table with default level `Bronze`
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pelanggan (id, level)
                    VALUES (%s, %s)
                """, [user_id, "Bronze"])

            # Success message and redirect
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # Replace with your login URL name

        except Exception as e:
            # Error handling
            messages.error(request, f"An error occurred: {e}")
            return redirect('register_pelanggan')  # Reload the registration page

    return render(request, 'register_pelanggan.html')


def register_pekerja(request):
    return render(request, 'register_pekerja.html')

def login_view(request):
    if request.method == 'POST':
        no_hp = request.POST['no_hp']
        password = request.POST['password']

        # Query to verify user in the `pengguna` table and get their ID
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nohp FROM pengguna 
                WHERE nohp = %s AND pwd = %s
            """, [no_hp, password])
            user_result = cursor.fetchone()

        if user_result:
            user_id, user_nohp = user_result

            # Determine user role by checking if ID exists in pelanggan or pekerja
            with connection.cursor() as cursor:
                # Check if user is a 'pelanggan'
                cursor.execute("SELECT EXISTS (SELECT 1 FROM pelanggan WHERE id = %s)", [user_id])
                is_pelanggan = cursor.fetchone()[0]

                if is_pelanggan:
                    request.session['user_role'] = 'pelanggan'  # Save role to session
                    response = render(request, 'main_pelanggan.html')
                    response.set_cookie('user_id', user_id)  # Set user ID cookie
                    return response

                # Check if user is a 'pekerja'
                cursor.execute("SELECT EXISTS (SELECT 1 FROM pekerja WHERE id = %s)", [user_id])
                is_pekerja = cursor.fetchone()[0]

                if is_pekerja:
                    request.session['user_role'] = 'pekerja'  # Save role to session
                    response = render(request, 'main_pekerja.html')
                    response.set_cookie('user_id', user_id)  # Set user ID cookie
                    return response

        # If login fails
        messages.error(request, 'Invalid credentials.')
        return redirect('login')

    return render(request, 'login.html')


@login_required
@csrf_exempt
def update_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            data = f"success,{user.full_name},{user.email},{user.age},{user.gender},{user.phone_number}"
            return HttpResponse(data, content_type='text/plain')
        else:
            errors = []
            for field, messages in form.errors.items():
                for message in messages:
                    errors.append(f"{field}:{message}")
            return HttpResponse("error," + ",".join(errors), content_type='text/plain', status=400)
    return HttpResponse("Method not allowed", status=405)

@login_required
@csrf_exempt
def update_photo(request):
    if request.method == 'POST':
        user = request.user
        new_photo_url = request.POST.get('profile_photo', '')

        # Periksa apakah URL valid (tidak kosong)
        if new_photo_url.strip():
            user.profile_photo = new_photo_url
            user.save()  # Simpan perubahan ke database
            return HttpResponse(f"success,{new_photo_url}", content_type='text/plain')
        else:
            return HttpResponse("error:Invalid URL", content_type='text/plain', status=400)
    return HttpResponse("Method not allowed", status=405)

@login_required
@csrf_exempt
def delete_photo(request):
    if request.method == 'POST':
        user = request.user
        user.profile_photo = None
        user.save()
        return HttpResponse("Photo deleted", content_type='text/plain')
    return HttpResponse("Method not allowed", status=405)

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Verifikasi password lama
        if not check_password(old_password, user.password):
            messages.error(request, 'Incorrect current password.', extra_tags='error')
            return redirect('change_password')

        # Validasi password baru
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.', extra_tags='error')
            return redirect('change_password')

        # Ubah password dan update session
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, 'Password changed successfully!', extra_tags='success')
        return redirect('change_password')
    
    return render(request, 'change_password.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'})

        user = authenticate(username=username, password=password)
        if user is not None and user == request.user:
            user.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid credentials.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
@role_required('customer')
def customer_dashboard(request):
    return render(request, 'main_customer.html')

@login_required
@role_required('customer')
def customer_categories(request):
    return render(request, 'categories.html')

@login_required
@role_required('admin')
def admin_categories(request):
    return render(request, 'categories_admin.html')

@login_required
def customer_blog(request):
    return render(request, 'blog/article_list.html')

@login_required
@role_required('admin')
def admin_dashboard(request):
    return render(request, 'main_admin.html')

def profile_pelanggan(request):
    # Get the user ID from the cookie
    user_id = request.COOKIES.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view your profile.")
        return redirect('login')

    try:
        # Fetch user details from the `pengguna` table
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

        # Unpack user details
        nama, jeniskelamin, nohp, tgllahir, alamat, saldomypay = user_data

        # Fetch user level from the `pelanggan` table
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT level 
                FROM pelanggan 
                WHERE id = %s
            """, [user_id])
            level_data = cursor.fetchone()

        level = level_data[0] if level_data else "Unknown"

        # Prepare context for the template
        context = {
            'nama': nama,
            'jeniskelamin': "Laki-laki" if jeniskelamin.lower() == 'l' else "Perempuan",
            'nohp': nohp,
            'tgllahir': tgllahir,
            'alamat': alamat,
            'level': level,
            'saldo': saldomypay  # Replace with actual balance retrieval logic if needed
        }

        return render(request, 'profile_pelanggan.html', context)

    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('login')


def profile_pekerja(request):
    # Get the user ID from the cookie
    user_id = request.COOKIES.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view your profile.")
        return redirect('login')

    try:
        # Fetch user details from the `pengguna` table
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

        # Unpack user details
        nama, jeniskelamin, nohp, tgllahir, alamat, saldomypay = user_data

        # Fetch additional details from the `pekerja` table
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

        # Prepare context for the template
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
        }

        return render(request, 'profile_pekerja.html', context)

    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('login')


def update_pelanggan(request):
    user = request.user
    return render(request, 'update_pelanggan.html')

def update_pekerja(request):
    user = request.user
    return render(request, 'update_pekerja.html')

def logout_view(request):
    # Create a response to redirect the user to the login page
    response = redirect('login')
    
    # Delete the `user_id` cookie
    response.delete_cookie('user_id')
    
    # Optionally, display a logout message
    messages.success(request, 'You have been logged out successfully.')
    
    return response