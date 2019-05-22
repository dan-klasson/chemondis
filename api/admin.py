from django.contrib import admin
from api.models import Interviewer


class InterviewerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Interviewer, InterviewerAdmin)
