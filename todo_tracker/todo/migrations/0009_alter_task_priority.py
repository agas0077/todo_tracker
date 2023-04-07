# Generated by Django 4.1.7 on 2023-03-18 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0008_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(3, 'Высокий'), (2, 'Средний'), (1, 'Низкий')], default=1),
        ),
    ]
