import factory
from . import models


class InterviewerFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Interviewer

    name = factory.Faker('name')
    email = factory.Faker('email')
