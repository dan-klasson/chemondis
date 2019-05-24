from django.test import TestCase
from rest_framework.test import APIClient
from ..factories import InterviewFactory, InterviewerFactory, TimeSlotFactory
from ..models import TimeSlot
from datetime import datetime
import factory.random
import json


class CreateSlotsTestCase(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.client = APIClient()

    def test_success(self):
        interview = InterviewFactory.create()
        interviewer = InterviewerFactory.create()
        interview.interviewers.add(interviewer)
        response = self.client.post(
            '/api/v1/slots/',
            {
                'interview_date': datetime(2000, 1, 1, 10, 0),
                'interview': interview.id
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(TimeSlot.objects.count(), 1)

    def test_interviewer_already_booked(self):
        interviews = InterviewFactory.create_batch(size=2)
        interviewer = InterviewerFactory.create()
        interviews[0].interviewers.add(interviewer)
        interviews[1].interviewers.add(interviewer)
        TimeSlotFactory.create(interview=interviews[1])
        response = self.client.post(
            '/api/v1/slots/',
            {
                'interview_date': datetime(2000, 1, 1, 10, 0),
                'interview': interviews[0].id
            }
        )
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            data.get('interview_date'),
            ['Slot is not longer available.']
        )

    def test_not_on_hour(self):
        interview = InterviewFactory.create()
        response = self.client.post(
            '/api/v1/slots/',
            {
                'interview_date': datetime(2000, 1, 1, 10, 5),
                'interview': interview.id
            }
        )
        data = json.loads(response.content)
        self.assertEqual(
            data.get('interview_date'),
            ["Datetime must be on the hour"]
        )
        self.assertEqual(response.status_code, 400)

    def test_not_on_hour__minutes(self):
        interview = InterviewFactory.create()
        response = self.client.post(
            '/api/v1/slots/',
            {
                'interview_date': datetime(2000, 1, 1, 10, 0, 5),
                'interview': interview.id
            }
        )
        data = json.loads(response.content)
        self.assertEqual(
            data.get('interview_date'),
            ["Datetime must be on the hour"]
        )
        self.assertEqual(response.status_code, 400)

    def test_not_valid_datetime_range(self):
        interview = InterviewFactory.create()
        response = self.client.post(
            '/api/v1/slots/',
            {
                'interview_date': datetime(2000, 1, 1, 22),
                'interview': interview.id
            }
        )
        data = json.loads(response.content)
        self.assertEqual(
            data.get('interview_date'),
            ["Invalid datetime range."]
        )
        self.assertEqual(response.status_code, 400)
