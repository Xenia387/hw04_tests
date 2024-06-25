# Тесты проекта Yatube
К данному проекту Yatube мной были написаны тесты для проверки работы моделей, форм, urls-адресов и view-функций

## Возможности проекта Yatube
Yatube - это социальная сеть для публикации постов. Можно публиковать, редактировать посты. Просмотривать посты в тематических группах, на страницах авторов и на главной странице. Оставлять комментарии к постам других авторов

# Технологии
- Python
- django-debug-toolbar==2.2
- django==2.2.16
- pytest-django==3.8.0
- pytest-pythonpath==0.7.3
- pytest==5.3.5
- requests==2.22.0
- six==1.14.0
- sorl-thumbnail==12.6.3
- mixer==7.1.2
- Faker==12.0.1

# Запуск проекта

- Клонируйте репозиторий с проектом на свой компьютер
```bash
git clone git@github.com:Xenia387/hw04_tests.git
```

```
cd hw04_tests
```

- Установите и активируйте виртуальное окружение

```
python3 -m venv env
```

```
source venv/bin/activate
```

  или

```
python -m venv env
```

```
source venv/Scripts/activate
```

- Установите зависимости из файла requirements.txt

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

- Выполните миграции

```
cd yatube
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```

- Выполните миграции

```
cd yatube
```

```
python manage.py makemigrations
```

```bash
python manage.py migrate
```

Автор: Анисимова Ксения
- email: anis.xenia@yandex.ru
- telegram: @Ksenia_An_mova
