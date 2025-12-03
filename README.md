#  Инструкция по запуску проекта

## 1. Клонирование репозитория

```bash
git clone https://github.com/maknot1/news_portal3
cd news_portal3
```

## 2. Создание виртуального окружения

```bash
python -m venv venv
```

### Активация окружения

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

## 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 4. Применение миграций

```bash
python manage.py migrate
```

## 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

## 6. Запуск сервера

```bash
python manage.py runserver
```

Открыть сайт:

```
http://127.0.0.1:8000/news/
```

Панель администратора:

```
http://127.0.0.1:8000/admin/
```

⚠️ Google / Yandex OAuth не работают без собственных ключей!
