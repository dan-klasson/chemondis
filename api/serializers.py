from rest_framework import serializers
from .models import Interview, Interviewer, TimeSlot
from .validators import IsValidHourValidator, IsOnTheHourValidator


class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = '__all__'


class InterviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interview
        fields = '__all__'
        validators = [
            IsValidHourValidator('start_hour', 'end_hour')
        ]


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'
        validators = [
            IsOnTheHourValidator(fields=['interview_date'])
        ]

    def create(self, validated_data):

        interview = Interview.objects.get(
            pk=validated_data.get('interview').id
        )

        date = validated_data.get('interview_date')

        # check the datetime is valid for this interview
        if date.hour < interview.start_hour or date.hour > interview.end_hour:
            raise serializers.ValidationError(
                {"interview_date": ["Invalid datetime range."]}
            )

        # check if interviewers for this interview have prior commitments
        if TimeSlot.objects.filter(
            interview_date=date,
            interview__interviewers__in=interview.interviewers.all()
        ).count():
            raise serializers.ValidationError(
                {"interview_date": ["Slot is not longer available."]}
            )

        return super().create(validated_data)
