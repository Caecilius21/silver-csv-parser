import numpy as np
from django.test import TestCase, Client
from django.urls import reverse
from .views import sinusoide

from rest_framework.test import APIRequestFactory, APIClient, RequestsClient
import random


class TestingAPI(TestCase):

    def test_create_req(self):
        factory = APIRequestFactory()
        request = factory.post(
            '/api/graph/', {'frequence': 10, 'amplitude': 10, 'temps': 10})

    def test_post_req(self):
        client = APIClient()
        response = client.post(
            '/api/graph/', {'frequence': 10, 'amplitude': 10, 'temps': 10})
        assert response.status_code == 200

    def test_get_req(self):
        client = APIClient()
        response = client.get('/api/graph/')
        assert response.status_code == 200


class TestingFrontend(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = reverse('homepage')


class TestingValues(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.temps = abs(random.random()) * 1000
        cls.amplitude = random.random() * 1000
        cls.frequency = abs(random.random()) * 1000

    def test_value(self):
        self.assertEqual(sinusoide(0, 0, 0), 0)

    def test_greater_amplitude(self):
        self.assertGreaterEqual(
            sinusoide(self.temps, self.amplitude, self.frequency), -self.amplitude)

    def test_greater_amplitude(self):
        self.assertLessEqual(
            sinusoide(self.temps, self.amplitude, self.frequency), self.amplitude)
