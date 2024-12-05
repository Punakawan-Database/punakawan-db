from django.shortcuts import render
from django.urls import *

# Create your views here.

categories = [
        {'name': 'Kategori 1', 'description': 'Ini Kategori 1', 'slug' : 'k1', 'subcategories': [
            {'name': 'Subkategori 1', 'description' : 'Ini Deskripsi Subkategori 1', 'slug': 'sk1'},
            {'name': 'Subkategori 2', 'description' : 'Ini Deskripsi Subkategori 2', 'slug': 'sk2'},
        ]},
        {'name': 'Kategori 2', 'description': 'Ini Kategori 2', 'slug' : 'k2', 'subcategories': [
            {'name': 'Subkategori 1', 'description' : 'Ini Deskripsi Subkategori 1', 'slug': 'sk1'},
            {'name': 'Subkategori 2', 'description' : 'Ini Deskripsi Subkategori 2', 'slug': 'sk2'},
        ]},
        {'name': 'Kategori 3', 'description': 'Ini Kategori 3', 'slug' : 'k3', 'subcategories': [
            {'name': 'Subkategori 1', 'description' : 'Ini Deskripsi Subkategori 1', 'slug': 'sk1'},
            {'name': 'Subkategori 2', 'description' : 'Ini Deskripsi Subkategori 2', 'slug': 'sk2'},
        ]},
    ]

service_sessions = [
        {
            'id': 1,
            'name': 'sesi servis 1 (2 hours)',
            'price': '150000'
        },
        {
            'id': 2,
            'name': 'sesi servis 2 (4 hours)',
            'price': '300000'
        },
        {
            'id': 3,
            'name': 'sesi servis 3 (6 hours)',
            'price': '450000'
        }
    ]

workers = [
        {
            'id': 1,
            'name': 'John Doe',
            'profile_picture': None
        },
        {
            'id': 2,
            'name': 'Jane Smith',
            'profile_picture': None
        },
        {
            'id': 3,
            'name': 'Bob Johnson',
            'profile_picture': None
        }
    ]

testimonials = [
        {
            'user_name': 'Alice Cooper',
            'date': '2024-03-10',
            'text': 'Great service! Very thorough and professional.',
            'rating': 5,
            'worker_name': 'John Doe'
        },
        {
            'user_name': 'David Brown',
            'date': '2024-03-08',
            'text': 'Good service but arrived a bit late.',
            'rating': 4,
            'worker_name': 'Jane Smith'
        }
    ]

def homepage(request):
    context = {
        'title' : 'Trust in Punakawan, because we dont trust ourselves',
        'categories': categories,
    }
    
    return render(request, 'homepage.html', context)

def subkategori_jasa(request, kategori_slug, subkategori_slug):
    # Find the matching category
    category = next((cat for cat in categories if cat['slug'] == kategori_slug), None)
    if not category:
        return render(request, '404.html', status=404)  # Return a 404 page if category not found
    
    # Find the matching subcategory within the category
    subcategory = next((sub for sub in category['subcategories'] if sub['slug'] == subkategori_slug), None)
    if not subcategory:
        return render(request, '404.html', status=404)  # Return a 404 page if subcategory not found
    
    # Pass the category and subcategory names to the template
    context = {
        'selected_category': category,
        'selected_subcategory': subcategory,
        'service_sessions': service_sessions,
        'workers': workers,
        'testimonials': testimonials
    }
    
    return render(request, 'subkategori.html', context)


def subkategori_jasa_pekerja(request, kategori_slug, subkategori_slug):
    # Find the matching category
    # category = next((cat for cat in categories if cat['slug'] == kategori_slug), None)
    # if not category:
    #     return render(request, '404.html', status=404)  # Return a 404 page if category not found
    
    # # Find the matching subcategory within the category
    # subcategory = next((sub for sub in category['subcategories'] if sub['slug'] == subkategori_slug), None)
    # if not subcategory:
    #     return render(request, '404.html', status=404)  # Return a 404 page if subcategory not found
    
    # Pass the category and subcategory names to the template
    context = {
        'selected_category': {'name': 'Kategori 4', 'description': 'Ini Kategori 4', 'slug' : 'k4'},
        'selected_subcategory': {'name': 'Subkategori 1', 'description' : 'Ini Deskripsi Subkategori 1', 'slug': 'sk1'},
        'service_sessions': service_sessions,
        'workers': workers,
        'testimonials': testimonials
    }
    
    return render(request, 'subkategori_pekerja.html', context)

orders = [
        {
            'id': 1,
            'subcategory': {'name': 'House Cleaning'},
            'service_session': {'name': 'Basic Cleaning (2 hours)'},
            'total_payment': '150000',
            'worker': {'name': 'John Doe'},
            'status': 'waiting_payment',
            'has_testimonial': False,
            'get_status_display': 'Menunggu Pembayaran'
        },
        {
            'id': 2,
            'subcategory': {'name': 'House Cleaning'},
            'service_session': {'name': 'Deep Cleaning (4 hours)'},
            'total_payment': '300000',
            'worker': None,
            'status': 'finding_worker',
            'has_testimonial': False,
            'get_status_display': 'Mencari Pekerja Terdekat'
        },
        {
            'id': 3,
            'subcategory': {'name': 'House Cleaning'},
            'service_session': {'name': 'Premium Cleaning (6 hours)'},
            'total_payment': '450000',
            'worker': {'name': 'Jane Smith'},
            'status': 'completed',
            'has_testimonial': False,
            'get_status_display': 'Pesanan Selesai'
        },
        {
            'id': 4,
            'subcategory': {'name': 'House Cleaning'},
            'service_session': {'name': 'Basic Cleaning (2 hours)'},
            'total_payment': '150000',
            'worker': {'name': 'Bob Johnson'},
            'status': 'completed',
            'has_testimonial': True,
            'get_status_display': 'Pesanan Selesai'
        }
    ]

def view_pemesanan(request):
    context = {
        'title' : 'Pemesanan',
        'orders': orders,
    }
    
    return render(request, 'pemesanan_jasa.html', context)