# todo_tracker
# :blue_book: Todo tracker на Django
> Pet-проект. 
> Разрабатывался для создания личного трекера задач, который бы обладал подходящим под потребности на текущей работе функционалом.
> Также целью проекта было углубить знания написания приложений на Django и REST API для добавления в портфолио.

## :triangular_ruler: Стек проекта: 
- Python 3.10 (Django, Django REST framework, Simple-JWT, djoser, drf-yasg)
- HTML5, Bootstrap 5, JS, CSS
- mySQL
- Ninja API
- Мidjourney

## :package: [Зависимости проекта](https://github.com/agas0077/todo_tracker/blob/master/requirements.txt)

## :wrench: Запуск проекта

- Создаём виртуальное окружение Python и активируем его

  ```
  $ python -m venv venv
  $ venv\Scripts\activate.bat - для Windows / source venv/bin/activate - для Linux и MacOS
  ```

- Устанавливаем зависимости проекта

  ```
  $ pip install -r requirements.txt
  ```

- Выполняем миграции бд

  ```
  $ python manage.py migrate
  ```
  
- Обычный запуск

  ```
  $ python manage.py runserver
  ``` 
  
> И определенно стоит настроить .env файл перед запуском

## :closed_lock_with_key: Настройка входа в админку

```
$ python manage.py createsuperuser --username admin@email.com --email admin@email.com
```

## :floppy_disk: Загрузка тестовых данных
Чтобы можно было посмотреть проект сразу заполненным - запускаем:
```
$ python manage.py load_data
```

## :sleeping: REST API Docs

API swagger:  ```http://.../swagger``` 