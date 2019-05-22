from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import RequestsClient
from .factories import InterviewerFactory
from .views import InterviewerViewSet
from .models import Interviewer
import factory.random
import json


class InterviewerTestCase(TestCase):

    viewset = InterviewerViewSet

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.client = APIClient()

    def test_retrieve(self):
        obj = InterviewerFactory.create()
        response = self.client.get('/api/v1/interviewers/{}/'.format(obj.id))
        data = json.loads(response.content)
        self.assertEqual(data['name'], 'Kari Patterson')
        self.assertEqual(data['email'], 'paulpadilla@williams.org')

    def test_list(self):
        InterviewerFactory.create_batch(size=5)
        response = self.client.get('/api/v1/interviewers/')
        data = json.loads(response.content)

        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]['name'], 'David Williams')
        self.assertEqual(data[0]['email'], 'pproctor@bowen-brooks.com')

    def test_create(self):
        self.client.post(
            '/api/v1/interviewers/',
            {'name': 'jane doe', 'email': 'jane@example.com'}
        )
        obj = Interviewer.objects.first()
        self.assertEqual(obj.name, 'jane doe')
        self.assertEqual(obj.email, 'jane@example.com')

    def test_create__empty(self):
        response = self.client.post(
            '/api/v1/interviewers/',
            {'name': '', 'email': ''}
        )
        data = json.loads(response.content)
        self.assertEqual(data.get('name'), ['This field may not be blank.'])
        self.assertEqual(data.get('email'), ['This field may not be blank.'])

    def test_create__invalid_email(self):
        response = self.client.post(
            '/api/v1/interviewers/',
            {'name': 'jane', 'email': 'invalid'}
        )
        data = json.loads(response.content)
        self.assertEqual(data.get('email'), ['Enter a valid email address.'])

    def test_update(self):
        obj = InterviewerFactory.create()
        self.client.put(
            '/api/v1/interviewers/{}/'.format(obj.id),
            {'name': 'jane doe', 'email': 'jane@example.com'}
        )
        obj = Interviewer.objects.first()
        self.assertEqual(obj.name, 'jane doe')
        self.assertEqual(obj.email, 'jane@example.com')

    def test_delete(self):
        obj = InterviewerFactory.create()
        self.assertEqual(Interviewer.objects.count(), 1)
        self.client.delete('/api/v1/interviewers/{}/'.format(obj.id))
        self.assertEqual(Interviewer.objects.count(), 0)
