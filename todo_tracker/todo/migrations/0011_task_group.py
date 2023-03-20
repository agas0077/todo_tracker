# Generated by Django 4.1.7 on 2023-03-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_alter_task_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='group',
            field=models.CharField(choices=[('work', 'Работа'), ('personal', 'Личное')], default='personal', max_length=10, verbose_name='Группа задачи'),
        ),
    ]