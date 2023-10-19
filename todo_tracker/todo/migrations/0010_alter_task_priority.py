# Generated by Django 4.1.7 on 2023-03-18 09:16

# Third Party Library
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(3, 'Высокий'), (2, 'Средний'), (1, 'Низкий')], default=1, verbose_name='Приоритет'),
        ),
    ]
