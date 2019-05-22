from rest_framework import serializers
from .models import Interview, Interviewer


class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = '__all__'


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'
