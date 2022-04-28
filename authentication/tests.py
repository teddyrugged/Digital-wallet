from django.test import TestCase
from django.contrib.auth import get_user_model 
from .models import Wallet


class RegisterTests(TestCase):
    
    def setUp(self):
            self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )
        
    def test_register_url_page(self):
        response = self.client.get('/api/v1/register/')   
        no_response = self.client.get('/posti/100000/')   
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(no_response.status_code, 404) 
