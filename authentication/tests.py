from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import reverse, status

from .models import User, Wallet


class RegisterTests(TestCase):
    
    def setUp(self):
        self.credentials = {'username':'testuser','email':'test@email.com','password':'secret124','first_name':'teddy','last_name':'biggy',}
        self.user = User.objects.create_user(**self.credentials)
        
    def test_register_url_page(self):
        response = self.client.get('/api/v1/register/')   
        no_response = self.client.get('/posti/100000/')   
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 
        self.assertEqual(no_response.status_code, status.HTTP_404_NOT_FOUND) 

    def test_user_values(self):
        self.assertEqual(f'{self.user.username}', 'testuser')
        self.assertEqual(f'{self.user.email}', 'test@email.com')
        self.assertEqual(f'{self.user.first_name}', 'teddy')
        self.assertEqual(f'{self.user.last_name}', 'biggy')
    
    def test_create_user(self):
        response = self.client.post('/api/v1/register/',{
            'username':'testuser2',
            'email':'2test@email.com',
            'password':'secret124',
            'first_name':'teddy',
            'last_name':'biggy', 
            'main_currency':1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        self.assertContains(response, 'testuser') 
        self.assertContains(response, 'teddy')
        
        
class LogInTest(TestCase):
    
    def setUp(self):
        self.credentials = {'username':'testuser','password':'secret124'}
        self.user = User.objects.create_user(**self.credentials)
        
    def test_view_login_page(self):
        response = self.client.get('/api/v1/login/')
        no_response = self.client.get('/post/100000/') 
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED) 
        self.assertEqual(no_response.status_code, status.HTTP_404_NOT_FOUND) 
        
    def test_login(self):
        response = self.client.post('/api/v1/login/', self.credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_fake_login_user(self):
        self.credentials = {
            'username': 'ahzn',
            'password':'sm393m49d'}
        response = self.client.post('/api/v1/login/', self.credentials,)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_user_cannot_register_with_no_data(self):
        response= self.client.post('/api/v1/login/', {})
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    






