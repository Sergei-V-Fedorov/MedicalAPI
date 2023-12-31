# MEDICAL API


## Разработать сервис терминологии и REST API к нему.
Существуют сервисы, которые обмениваются между собой электронными документами. Электронный документ представляет собой структуру в формате
JSON.
Чтобы данные в полях таких документов были понятны принимающей системе и трактовались однозначно всеми участниками обмена, помимо структуры
документа, необходимо прийти к общему соглашению кодирования контекста данных.
Для этого потребуется независимый сервис терминологии, который хранит коды данных и их контекст. Проще говоря, это база данных справочников, с
кодами и значениями.

### Требования к окружению
  * Версия Python >= 3.10

### Установка зависимостей
* Установка зависимостей:
```commandline
pip install -r requirements.txt
```

### Создание учетной записи администратора
```commandline
python manage.py migrate
```
```commandline
python manage.py createsuperuser
```
 - Login: admin
 - password: admin
 - email: -

### Создание базы данных
```commandline
python manage.py makemigrations
```
```commandline
python manage.py migrate
```

### Загрузка фикстур
```commandline
python manage.py loaddata guides/fixtures/guides.json
```

### Запуск приложения
```commandline
python manage.py runserver
```

### Вход в административную панель:
 - Login: admin
 - password: admin
### Примеры доступных API
* Список всех доступных справочников 
 - http://127.0.0.1:8000/refbooks/
 * Список справочников отфильтрованных по дате 
 - http://127.0.0.1:8000/refbooks/?date=2023-06-01 
 * Получение элементов справочника
 - http://127.0.0.1:8000/refbooks/1/elements/ 
 * Получение элементов справочника с версией 1.0
 - http://127.0.0.1:8000/refbooks/1/elements/?version=1.0 
 * проверка существования элемента с кодом и значением в конкретной версии справочника. 
 - http://127.0.0.1:8000/refbooks/1/check_element/?code=2&value=хирург
 - http://127.0.0.1:8000/refbooks/1/check_element/?code=4&value=офтальмолог
 - http://127.0.0.1:8000/refbooks/1/check_element/?code=1&value=врач-терапевт&version=1.0
 * Документация к API
 - http://127.0.0.1:8000/api/schema/swagger/
