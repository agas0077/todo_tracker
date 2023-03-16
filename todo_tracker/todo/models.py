from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    text = models.TextField('Задание')
    create_date = models.DateTimeField('Дата создания', auto_now_add=True)
    deadline_date = models.DateTimeField('Дата дедлайна')
    # created_by = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='tasks')
    image = models.ImageField(
        'Картинка', upload_to='todo/', null=True, blank=True)
    completed = models.BooleanField('Завершено', default=False)

    class Meta:
        ordering = ('-create_date',)

    def __str__(self):
        return self.text
