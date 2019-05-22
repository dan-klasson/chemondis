from rest_framework import viewsets
from .serializers import InterviewerSerializer
from .models import Interviewer


class InterviewerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows interviewers to be
    retrieved, listed, added and edited.
    """
    queryset = Interviewer.objects.all().order_by('name')
    serializer_class = InterviewerSerializer
