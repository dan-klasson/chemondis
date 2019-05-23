from django.test import TestCase
from freezegun import freeze_time
from rest_framework.test import APIClient
from ..factories import InterviewFactory, InterviewerFactory, TimeSlotFactory
from ..models import TimeSlot
from datetime import datetime
import factory.random
import json


class ListSlotsTestCase(TestCase):

    def setUp(self):
        factory.random.reseed_random('chemondis')
        self.client = APIClient()

    def url(self, interview):
        return '/api/v1/interviews/{}/slots/'.format(interview.id)

    def test_success(self):
        interview = InterviewFactory.create()
        response = self.client.get(self.url(interview))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data.get('slots')), 160)

    def test_start_end_date(self):
        interview = InterviewFactory.create(
            start_date=datetime(2000, 1, 1, 10),
            end_date=datetime(2000, 1, 1, 11),
        )
        response = self.client.get(self.url(interview))
        data = json.loads(response.content)
        self.assertEqual(len(data.get('slots')), 20)

    def test_slot_days(self):
        interview = InterviewFactory.create(slot_days=1)
        response = self.client.get(self.url(interview))
        data = json.loads(response.content)
        self.assertEqual(len(data.get('slots')), 8)

    @freeze_time("1999-12-31")
    def test_interviewer_already_booked(self):
        interviewer = InterviewerFactory.create()
        interview = InterviewFactory.create(slot_days=1)
        interview.interviewers.add(interviewer)
        TimeSlotFactory.create(interview=interview)

        response = self.client.get(self.url(interview))
        data = json.loads(response.content)
        self.assertEqual(len(data.get('slots')), 7)
