import factory
from . import models
from datetime import datetime


class InterviewerFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Interviewer

    name = factory.Faker('name')
    email = factory.Faker('email')


class InterviewFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Interview

    candidate_name = factory.Faker('name')
    candidate_email = factory.Faker('email')


class TimeSlotFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.TimeSlot

    interview_date = datetime(2000, 1, 1, 10, 0)
    interview = factory.SubFactory(InterviewFactory)
