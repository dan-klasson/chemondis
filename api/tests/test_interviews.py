from django.test import TestCase
from rest_framework.test import APIClient
from ..factories import InterviewFactory, InterviewerFactory
from ..models import Interview
from datetime import datetime
import factory.random
import json


class InterviewTestCase(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.client = APIClient()
        self.interviewer1 = InterviewerFactory.create()
        self.interviewer2 = InterviewerFactory.create()
        self.interviewers_ids = [self.interviewer1.id, self.interviewer2.id]


    def create(self,
        candidate_name='jane doe',
        candidate_email='jane@example.com',
        start_hour=9,
        end_hour=17,
        interviewers=None):

        return self.client.post('/api/v1/interviews/', {
            'candidate_name': candidate_name,
            'candidate_email': candidate_email,
            'start_hour': start_hour,
            'end_hour': end_hour,
            'interviewers': interviewers or self.interviewers_ids
        })

    def test_retrieve(self):
        obj = InterviewFactory.create()
        obj.interviewers.add(self.interviewer1, self.interviewer2)

        response = self.client.get('/api/v1/interviews/{}/'.format(obj.id))
        data = json.loads(response.content)
        self.assertEqual(data['candidate_name'], 'Theresa Adkins')
        self.assertEqual(data['candidate_email'], 'megan32@martin.biz')
        self.assertEqual(data['start_hour'], 9)
        self.assertEqual(data['end_hour'], 17)
        self.assertEqual(data['interviewers'], self.interviewers_ids)

    def test_list(self):
        objs = InterviewFactory.create_batch(size=5)
        objs[0].interviewers.add(self.interviewer1, self.interviewer2)
        response = self.client.get('/api/v1/interviews/')
        data = json.loads(response.content)

        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]['candidate_name'], 'Theresa Adkins')
        self.assertEqual(
            data[0]['candidate_email'], 'megan32@martin.biz'
        )
        self.assertEqual(data[0]['interviewers'], self.interviewers_ids)

    def test_create(self):
        self.create()
        obj = Interview.objects.first()
        self.assertEqual(obj.candidate_name, 'jane doe')
        self.assertEqual(obj.candidate_email, 'jane@example.com')
        self.assertEqual(obj.start_hour, 9)
        self.assertEqual(obj.end_hour, 17)
        self.assertEqual(obj.interviewers.first().id, self.interviewer1.id)
        self.assertEqual(obj.interviewers.last().id, self.interviewer2.id)

    def test_create__empty(self):
        self.interviewers_ids = ''
        response = self.create(
            candidate_name='',
            candidate_email='',
        )
        data = json.loads(response.content)
        blank = ['This field may not be blank.']
        self.assertEqual(data.get('candidate_name'), blank)
        self.assertEqual(data.get('candidate_email'), blank)
        self.assertEqual(
            data.get('interviewers'),
            ['Incorrect type. Expected pk value, received str.']
        )

    def test_create__null(self):
        response = self.client.post('/api/v1/interviews/')
        data = json.loads(response.content)
        required = ['This field is required.']
        self.assertEqual(data.get('candidate_name'), required)
        self.assertEqual(data.get('candidate_email'), required)
        self.assertEqual(data.get('interviewers'), required)

    def test_create__invalid_email(self):
        response = self.create(
            candidate_name='jane',
            candidate_email='invalid'
        )
        data = json.loads(response.content)
        self.assertEqual(
            data.get('candidate_email'),
            ['Enter a valid email address.']
        )

    def test_create__invalid_interviewers(self):
        response = self.create(interviewers=123)
        data = json.loads(response.content)
        self.assertEqual(
            data.get('interviewers'),
            ['Invalid pk "123" - object does not exist.']
        )

    def test_create__invalid_start_hour(self):
        response = self.create(start_hour=-5)
        data = json.loads(response.content)
        self.assertEqual(
            data.get('start_hour'),
            ['Invalid start hour specified.']
        )

    def test_create__invalid_end_hour(self):
        response = self.create(end_hour=25)
        data = json.loads(response.content)
        self.assertEqual(
            data.get('end_hour'),
            ['Invalid end hour specified.']
        )

    def test_create__invalid_start_and_end_hour(self):
        response = self.create(start_hour=20, end_hour=20)
        data = json.loads(response.content)
        self.assertEqual(
            data.get('start_hour'),
            ["Start can't be greater or equal to end hour."]
        )

    def test_update(self):
        obj = InterviewFactory.create()
        self.client.put(
            '/api/v1/interviews/{}/'.format(obj.id),
            {
                'candidate_name': 'jane doe',
                'candidate_email': 'jane@example.com',
                'start_hour': 10,
                'end_hour': 18,
                'interviewers': self.interviewers_ids
            }
        )
        obj = Interview.objects.first()
        self.assertEqual(obj.candidate_name, 'jane doe')
        self.assertEqual(obj.candidate_email, 'jane@example.com')
        self.assertEqual(obj.start_hour, 10)
        self.assertEqual(obj.end_hour, 18)
        self.assertEqual(obj.interviewers.first().id, self.interviewer1.id)
        self.assertEqual(obj.interviewers.last().id, self.interviewer2.id)

    def test_delete(self):
        obj = InterviewFactory.create()
        self.assertEqual(Interview.objects.count(), 1)
        self.client.delete('/api/v1/interviews/{}/'.format(obj.id))
        self.assertEqual(Interview.objects.count(), 0)
