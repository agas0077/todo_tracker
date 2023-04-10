import csv
import datetime as dt
import os
import shutil
import random


from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from todo_tracker.settings import BASE_DIR, MEDIA_ROOT, Path
from todo.models import Task
DATE_FORMAT = 'YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]'
DATE_FORMAT = r'%d.%m.%Y'
User = get_user_model()


class Command(BaseCommand):
    """ Пакетная загрузка данных в базу"""

    def handle(self, *args, **kwargs):
        try:
            print(self.users_load())
            print(self.task_load())
            print(self.images_load())
        except Exception as error:
            raise Exception(f'Ошибка загрузки {error}')

    def task_load(self):
        file_to_load = Path(BASE_DIR, 'static', 'test_data', 'test_tasks.csv')
        with file_to_load.open(encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            count = 0
            Task.objects.all().delete()
            for row in file_reader:
                if count == 0:
                    print(f'Task содержит столбцы: {", ".join(row)}')
                else:
                    Task.objects.create(
                        title=row[0],
                        text=row[1],
                        create_date=dt.datetime.strptime(row[2], DATE_FORMAT),
                        deadline_date=dt.datetime.strptime(
                            row[3], DATE_FORMAT),
                        created_by=User.objects.get(pk=int(row[4])),
                        image=row[5],
                        completed=bool(int(row[6])),
                        priority=row[7],
                        group=row[8],
                    )
                count += 1

        return f'Загрузка Task - {count} строк(и)'

    def users_load(self):
        file_to_load = Path(BASE_DIR, 'static', 'test_data', 'test_users.csv')
        with file_to_load.open(encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            count = 0
            User.objects.all().delete()
            for row in file_reader:
                if count == 0:
                    print(f'Users содержит столбцы: {", ".join(row)}')
                else:
                    User.objects.create(
                        password=make_password(row[0]),
                        id=row[1],
                        username=row[2],
                        last_name=row[3],
                        email=row[4],
                        first_name=row[5],
                    )
                count += 1

        return f'Загрузка Users - {count} строк(и)'

    def images_load(self):
        img_to_load = Path(BASE_DIR, 'static', 'test_data', 'images')
        items = list(Task.objects.all())
        # if you want only a single random item
        random_item = random.choice(items)
        random_items = random.sample(items, int(len(items)) // 3)

        count = 0
        all_image_paths = []
        for file in os.listdir(img_to_load):
            from_path = os.path.join(img_to_load, file)
            to_path = os.path.join(MEDIA_ROOT, 'todo', f'{random.randint(0, 19999999)}.jpg')
            shutil.copy2(from_path, to_path)
            all_image_paths.append(to_path)
            count += 1
        print(all_image_paths)
        for task in items:
            path = random.choice(all_image_paths)
            task.image = os.path.join(*path.split('\\')[-2:])
            task.save()

        
        return f'Загрузка {count} картинок'
