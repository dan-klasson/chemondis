from rest_framework import serializers


class IsOnTheHourValidator:

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, dic):
        errors = []
        for field in self.fields:
            dt = dic.get(field)
            if dt.minute != 0 or dt.second != 0:
                raise serializers.ValidationError(
                    {field: ["Datetime must be on the hour"]}
                )


class IsSameDate:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, dic):
        dt1 = dic.get(self.field1)
        dt2 = dic.get(self.field2)
        if dt1.date() != dt2.date():
            err = "'{}' needs to be the same date as '{}'"
            raise serializers.ValidationError({
                self.field1: [err.format(self.field1, self.field2)]
            })
