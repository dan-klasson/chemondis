from rest_framework import serializers


class IsOnTheHourValidator:
    def __call__(self, dic):
        dt = dic.get('interview_date')
        if dt.minute != 0 or dt.second != 0:
            raise serializers.ValidationError(
                {"interview_date": ["Datetime must be on the hour"]}
            )
