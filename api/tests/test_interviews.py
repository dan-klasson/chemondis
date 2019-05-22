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

    def test_retrieve(self):
        obj = InterviewFactory.create()
        obj.interviewers.add(self.interviewer1, self.interviewer2)

        response = self.client.get('/api/v1/interviews/{}/'.format(obj.id))
        data = json.loads(response.content)
        self.assertEqual(data['candidate_name'], 'Theresa Adkins')
        self.assertEqual(data['candidate_email'], 'megan32@martin.biz')
        self.assertEqual(data['hours'], 1)
        self.assertEqual(data['start_date'], '2000-01-01T09:00:00')
        self.assertEqual(data['end_date'], '2000-01-01T17:00:00')
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
        self.client.post(
            '/api/v1/interviews/',
            {
                'candidate_name': 'jane doe',
                'candidate_email': 'jane@example.com',
                'hours': 2,
                'start_date': datetime(2002, 2, 2, 10, 0),
                'end_date': datetime(2002, 2, 2, 18, 0),
                'interviewers': self.interviewers_ids
            }
        )
        obj = Interview.objects.first()
        self.assertEqual(obj.candidate_name, 'jane doe')
        self.assertEqual(obj.candidate_email, 'jane@example.com')
        self.assertEqual(obj.hours, 2)
        self.assertEqual(obj.start_date, datetime(2002, 2, 2, 10, 0))
        self.assertEqual(obj.end_date, datetime(2002, 2, 2, 18, 0))
        self.assertEqual(obj.interviewers.first().id, self.interviewer1.id)
        self.assertEqual(obj.interviewers.last().id, self.interviewer2.id)

    def test_create__empty(self):
        response = self.client.post(
            '/api/v1/interviews/',
            {
                'candidate_name': '',
                'candidate_email': '',
                'start_date': '',
                'end_date': '',
                'interviewers': ''
            }
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
        self.assertEqual(data.get('start_date'), required)
        self.assertEqual(data.get('end_date'), required)
        self.assertEqual(data.get('interviewers'), required)

    def test_create__invalid_email(self):
        response = self.client.post(
            '/api/v1/interviews/',
            {'candidate_name': 'jane', 'candidate_email': 'invalid'}
        )
        data = json.loads(response.content)
        self.assertEqual(
            data.get('candidate_email'),
            ['Enter a valid email address.']
        )

    def test_create__invalid_interviewers(self):
        response = self.client.post(
            '/api/v1/interviews/',
            {'interviewers': 123}
        )
        data = json.loads(response.content)
        self.assertEqual(
            data.get('interviewers'),
            ['Invalid pk "123" - object does not exist.']
        )

    def test_update(self):
        obj = InterviewFactory.create()
        self.client.put(
            '/api/v1/interviews/{}/'.format(obj.id),
            {
                'candidate_name': 'jane doe',
                'candidate_email': 'jane@example.com',
                'hours': 3,
                'start_date': datetime(2002, 2, 2, 10, 0),
                'end_date': datetime(2002, 2, 2, 18, 0),
                'interviewers': self.interviewers_ids
            }
        )
        obj = Interview.objects.first()
        self.assertEqual(obj.candidate_name, 'jane doe')
        self.assertEqual(obj.candidate_email, 'jane@example.com')
        self.assertEqual(obj.hours, 3)
        self.assertEqual(obj.start_date, datetime(2002, 2, 2, 10, 0))
        self.assertEqual(obj.end_date, datetime(2002, 2, 2, 18, 0))
        self.assertEqual(obj.interviewers.first().id, self.interviewer1.id)
        self.assertEqual(obj.interviewers.last().id, self.interviewer2.id)

    def test_delete(self):
        obj = InterviewFactory.create()
        self.assertEqual(Interview.objects.count(), 1)
        self.client.delete('/api/v1/interviews/{}/'.format(obj.id))
        self.assertEqual(Interview.objects.count(), 0)
