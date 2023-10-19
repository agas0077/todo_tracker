# Third Party Library
# Create your models here.
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Task(models.Model):
    class Priority(models.IntegerChoices):
        HIGH = 3, _("Высокий")
        MEDIUM = 2, _("Средний")
        LOW = 1, _("Низкий")

    class Group(models.TextChoices):
        WORK = "work", _("Работа")
        PERSONAL = "personal", _("Личное")

    title = models.CharField("Название", max_length=200, blank=True)
    text = models.TextField("Задание")
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)
    deadline_date = models.DateTimeField("Дата дедлайна")
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    image = models.ImageField(
        "Картинка", upload_to="todo/", null=True, blank=True
    )
    completed = models.BooleanField("Завершено", default=False)
    priority = models.IntegerField(
        "Приоритет", choices=Priority.choices, default=Priority.LOW
    )
    group = models.CharField(
        "Группа задачи",
        choices=Group.choices,
        default=Group.PERSONAL,
        max_length=10,
    )

    class Meta:
        ordering = ("-create_date",)

    def __str__(self):
        return self.text
