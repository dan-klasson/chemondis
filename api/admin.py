from django.contrib import admin
from api.models import Interviewer, Interview, TimeSlot


class InterviewerAdmin(admin.ModelAdmin):
    pass


class InterviewAdmin(admin.ModelAdmin):
    pass


class TimeSlotAdmin(admin.ModelAdmin):
    list_select_related = ['interview']


admin.site.register(Interviewer, InterviewerAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
