from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('main/', views.customer_dashboard, name='customer_dashboard'),
    path('categories/', views.customer_categories, name='customer_categories'),
    path('blog/', views.customer_blog, name='customer_blog'),    
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-categories/', views.admin_categories, name='admin_categories'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-photo/', views.update_photo, name='update_photo'),
    path('delete-photo/', views.delete_photo, name='delete_photo'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
]
