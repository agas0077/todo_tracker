
# Register your models here.
from django.contrib import admin
from todo.models import Task
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'create_date',
        'deadline_date',
        # 'created_by',
    )
    empty_value_display = '-пусто-'

admin.site.register(Task, TaskAdmin)