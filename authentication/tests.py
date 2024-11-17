from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com',
            'full_name': 'Test User',
            'age': 25,
            'gender': 'Male',
            'phone_number': '08123456789',
            'role': 'customer',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'age': 30,
            'gender': 'FEMALE',
            'phone_number': '08129876543',
            'role': 'customer',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_login_user_success(self):
        response = self.client.post(reverse('login'), {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_dashboard'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_user_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_logout_user(self):
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('main:show_main'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'testuser@example.com',
            'full_name': 'Test User',
            'age': 25,
            'gender': 'Male',
            'phone_number': '08123456789',
            'role': 'customer',
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.client.login(username=self.user_data['username'], password=self.user_data['password'])

    def test_update_profile(self):
        response = self.client.post(reverse('update_profile'), {
            'full_name': 'Updated Name',
            'email': 'updated@example.com',
            'age': 30,
            'gender': 'Female',
            'phone_number': '08129876543',
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.full_name, 'Updated Name')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_update_photo(self):
        response = self.client.post(reverse('update_photo'), {
            'profile_photo': 'https://example.com/photo.jpg',
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.profile_photo, 'https://example.com/photo.jpg')

    def test_delete_photo(self):
        self.user.profile_photo = 'https://example.com/photo.jpg'
        self.user.save()
        response = self.client.post(reverse('delete_photo'))
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.user.profile_photo)

    def test_change_password(self):
        response = self.client.post(reverse('change_password'), {
            'old_password': 'testpassword123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123',
        })
        self.assertRedirects(response, reverse('change_password'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_delete_account(self):
        response = self.client.post(reverse('delete_account'), {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
            'confirm_password': self.user_data['password'],
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(username='testuser').exists())

    def test_customer_dashboard_access(self):
        self.user.role = 'customer'
        self.user.save()
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_access_denied(self):
        self.user.role = 'customer'
        self.user.save()
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 403)

    def test_admin_dashboard_access_granted(self):
        self.user.role = 'admin'
        self.user.save()
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_customer_categories_access(self):
        self.user.role = 'customer'
        self.user.save()
        response = self.client.get(reverse('customer_categories'))
        self.assertEqual(response.status_code, 200)

    def test_admin_categories_access(self):
        self.user.role = 'admin'
        self.user.save()
        response = self.client.get(reverse('admin_categories'))
        self.assertEqual(response.status_code, 200)
    
    def test_customer_blog_access(self):
        response = self.client.get(reverse('customer_blog'))
        self.assertEqual(response.status_code, 200)

    def test_profile_access(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.full_name)

