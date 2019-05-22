from django.db import models


class Interviewer(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField()

    def __str__(self):
        return "{} <{}>".format(self.name, self.email)


class Interview(models.Model):
    candidate_name = models.CharField(max_length=254)
    candidate_email = models.EmailField()
    hours = models.IntegerField(default=1)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    interviewers = models.ManyToManyField(Interviewer)

    def __str__(self):
        return "{} <{}>".format(self.candidate_name, self.candidate_email)


class TimeSlot(models.Model):
    interview_date = models.DateTimeField(db_index=True)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
