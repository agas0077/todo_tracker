# Generated by Django 4.1.7 on 2023-03-15 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_task_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='created_by',
        ),
    ]
