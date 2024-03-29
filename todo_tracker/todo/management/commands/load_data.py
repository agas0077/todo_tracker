# Standard Library
import csv
import datetime as dt
import os
import random
import shutil

# Third Party Library
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from todo.models import Task

from todo_tracker.settings import BASE_DIR, MEDIA_ROOT, Path

DATE_FORMAT = r"%d.%m.%Y"
User = get_user_model()


class Command(BaseCommand):
    """Пакетная загрузка данных в базу"""

    def handle(self, *args, **kwargs):
        try:
            print(self.users_load())
            print(self.task_load())
            print(self.images_load())
        except Exception as error:
            raise Exception(f"Ошибка загрузки {error}")

    def task_load(self):
        file_to_load = Path(BASE_DIR, "static", "test_data", "test_tasks.csv")
        with file_to_load.open(encoding="utf-8") as r_file:
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
                            row[3], DATE_FORMAT
                        ),
                        created_by=User.objects.get(pk=int(row[4])),
                        image=row[5],
                        completed=bool(int(row[6])),
                        priority=row[7],
                        group=row[8],
                    )
                count += 1

        return f"Загрузка Task - {count} строк(и)"

    def users_load(self):
        file_to_load = Path(BASE_DIR, "static", "test_data", "test_users.csv")
        with file_to_load.open(encoding="utf-8") as r_file:
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

        return f"Загрузка Users - {count} строк(и)"

    def images_load(self):
        img_to_load = Path(BASE_DIR, "static", "test_data", "images")
        items = list(Task.objects.all())

        all_image_paths = []

        save_to_path = os.path.join(MEDIA_ROOT, "todo")
        if not os.path.exists(save_to_path):
            os.makedirs(save_to_path, exist_ok=True)

        for file in os.listdir(img_to_load):
            from_path = os.path.join(img_to_load, file)

            to_path = os.path.join(
                save_to_path, f"{random.getrandbits(128)}.jpg"
            )

            shutil.copy2(from_path, to_path)
            all_image_paths.append(to_path)

        count = 0
        for task in items:
            add_image = random.choice([True, False])
            if add_image:
                path = random.choice(all_image_paths)
                task.image = os.path.join(*path.split("\\")[-2:])
                task.save()
                count += 1

        return f"Загрузка {count} картинок"
