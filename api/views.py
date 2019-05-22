from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView
from .serializers import (
    InterviewSerializer, InterviewerSerializer
)
from .models import Interview, Interviewer, TimeSlot


class InterviewerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows interviewers to be
    retrieved, listed, added and edited.
    """
    queryset = Interviewer.objects.all().order_by('name')
    serializer_class = InterviewerSerializer


class InterviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows interviews to be
    retrieved, listed, added and edited.
    """
    queryset = Interview.objects.all().order_by('start_date')
    serializer_class = InterviewSerializer
