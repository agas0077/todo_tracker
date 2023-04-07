import base64
import datetime as dt

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from todo.models import Task
from error_messages.ValidationErrors import DEADLINE_ERROR


class DateField(serializers.DateTimeField):

    def to_internal_value(self, value):
        value = dt.datetime.strptime(value, r'%Y-%m-%d')
        return super().to_internal_value(value)

    def to_representation(self, value):
        value = value.date()
        return value


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TaskSerializer(serializers.ModelSerializer):
    created_by = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    create_date = DateField(required=False, read_only=True)
    deadline_date = DateField(required=True)

    class Meta:
        fields = '__all__'
        model = Task

    def validate_deadline_date(self, value):
        if value.timestamp() < dt.datetime.now().timestamp():
            raise serializers.ValidationError(DEADLINE_ERROR)
        return value
