from rest_framework import serializers


class IsOnTheHourValidator:

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, dic):
        for field in self.fields:
            dt = dic.get(field)
            if dt.minute != 0 or dt.second != 0:
                raise serializers.ValidationError(
                    {field: ["Datetime must be on the hour"]}
                )


class IsValidHourValidator:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, dic):
        start_hour = dic.get(self.field1)
        end_hour = dic.get(self.field2)
        if start_hour and start_hour < 0:
            raise serializers.ValidationError({
                "start_hour": ["Invalid start hour specified."]
            })
        if end_hour and end_hour > 24:
            raise serializers.ValidationError({
                "end_hour": ["Invalid end hour specified."]
            })
        if start_hour and end_hour and start_hour >= end_hour:
            raise serializers.ValidationError({
                "start_hour": ["Start can't be greater or equal to end hour."]
            })
