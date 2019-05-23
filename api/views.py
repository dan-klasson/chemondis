from rest_framework import viewsets, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import (
    InterviewSerializer, InterviewerSerializer, TimeSlotSerializer
)
from .models import Interview, Interviewer, TimeSlot


class InterviewerViewSet(viewsets.ModelViewSet):
    """
    Retrieve, list, add and edit the people holding the interview.
    """
    queryset = Interviewer.objects.all().order_by('name')
    serializer_class = InterviewerSerializer


class InterviewViewSet(viewsets.ModelViewSet):
    """
    Retrieve, list, add and edit interviews.
    """
    queryset = Interview.objects.all().order_by('start_date')
    serializer_class = InterviewSerializer


class TimeSlotCreateViewSet(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    """
    Create time slots for interviews.
    """
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer


class TimeSlotListViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    List time slots by interview
    """
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

    def list(self, request, interview_pk=None, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        interview = Interview.objects.get(pk=interview_pk)
        slots = interview.available_slots(queryset)

        return Response({"slots": slots})
