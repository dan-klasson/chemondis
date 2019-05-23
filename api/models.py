from django.db import models
from datetime import datetime, timedelta


class Interviewer(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField()

    def __str__(self):
        return "{} <{}>".format(self.name, self.email)


class Interview(models.Model):
    candidate_name = models.CharField(max_length=254)
    candidate_email = models.EmailField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slot_days = models.IntegerField(default=20)
    interviewers = models.ManyToManyField(Interviewer)

    def __str__(self):
        return "{} <{}>".format(self.candidate_name, self.candidate_email)

    def available_slots(self, slots_qs):

        # all slots already booked for the interviewers of this interview
        slots_to_exclude = slots_qs.filter(
            interview__interviewers__in=self.interviewers.all()
        ).values_list('interview_date', flat=True)

        available = []
        for day in range(0, self.slot_days):
            date = datetime.now() + timedelta(days=day + 1)
            for hour in range(self.start_date.hour, self.end_date.hour):
                dt = datetime(date.year, date.month, date.day, hour)
                if dt not in slots_to_exclude:
                    available.append(dt)
        return available


class TimeSlot(models.Model):
    interview_date = models.DateTimeField(db_index=True)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(
            self.interview.candidate_name,
            self.interview_date.strftime("%d %b %Y %H:%M")
        )
