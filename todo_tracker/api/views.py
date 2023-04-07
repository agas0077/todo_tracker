from rest_framework.viewsets import ModelViewSet

from api import serializers
from todo.models import Task


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        return self.request.user.tasks.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
