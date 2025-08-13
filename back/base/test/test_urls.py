# base/tests/test_urls.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from base.models import Business, Service, Booking, Customer

User = get_user_model()

class BaseURLsTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.business_owner = User.objects.create_user(
            email='owner@test.com',
            password='testpass123',
            user_type='business_owner'
        )
        self.customer_user = User.objects.create_user(
            email='customer@test.com',
            password='testpass123',
            user_type='customer'
        )
        
        # Create test business
        self.business = Business.objects.create(
            owner=self.business_owner,
            name='Test Business',
            slug='test-business',
            email='business@test.com',
            phone='1234567890',
            address='123 Test St',
            city='Test City',
            state='TS',
            country='Test Country',
            postal_code='12345',
            category='Test Category'
        )
    
    def test_business_list_url(self):
        """Test business list endpoint"""
        url = reverse('base:business-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_business_detail_url(self):
        """Test business detail endpoint"""
        url = reverse('base:business-detail', kwargs={'slug': self.business.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_business_dashboard_requires_auth(self):
        """Test dashboard endpoint requires authentication"""
        url = reverse('base:business-dashboard', kwargs={'slug': self.business.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_booking_create_requires_auth(self):
        """Test booking creation requires authentication"""
        url = reverse('base:booking-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_customer_me_endpoint(self):
        """Test customer me endpoint"""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse('base:customer-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)