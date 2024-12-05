import datetime
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

def register(request):
    return render(request, 'register.html')
  
def register_user(request):
    return render(request, 'register_user.html')

def register_worker(request):
    return render(request, 'register_worker.html')

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
                    # Render template for pelanggan
                    return render(request, 'main_pelanggan.html')

                # Check if user is a 'pekerja'
                cursor.execute("SELECT EXISTS (SELECT 1 FROM pekerja WHERE id = %s)", [user_id])
                is_pekerja = cursor.fetchone()[0]

                if is_pekerja:
                    # Render template for pekerja
                    return render(request, 'main_pekerja.html')

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
    user = request.user
    return render(request, 'profile_pelanggan.html', {'user': user})

def profile_pekerja(request):
    user = request.user
    return render(request, 'profile_pekerja.html', {'user': user})

def update_pengguna(request):
    user = request.user
    return render(request, 'update_pengguna.html')

def update_pekerja(request):
    user = request.user
    return render(request, 'update_pekerja.html')

def logout_user(request):
    logout(request)
    response = redirect('main:show_main')
    response.delete_cookie('last_login')
    return response