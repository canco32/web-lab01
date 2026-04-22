# REAL CHAT API

**Студент:** Сілін Ілля Денисович  
**Група:** КВ-52мп  
**Лабораторна робота:** №1 - Розробка серверної частини Web-додатка

## Опис завдання
Розробити серверну частину Web-додатку для чату (приватні та групові бесіди, повідомлення) з використанням Django та Django REST Framework.

## Посилання на звіт
[Звіт на Google Drive](https://docs.google.com/document/d/124v5UraF6AW4cGQnOgFNij1rfJJpu9LfbP0RXUzUMVY/edit?usp=sharing)

## Встановлення та запуск

1. Клонування репозиторію:
```bash
git clone https://github.com/canco32/web-lab01.git
cd web-lab01
```

2. Створення віртуального середовища:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Встановлення залежностей:
```bash
pip install -U pip
pip install -r requirements.txt
```

4. Міграції бази даних:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Запуск сервера:
```bash
python manage.py runserver
```

## API Документація
http://127.0.0.1:8000/api/docs/

## Основні endpoints
- `POST /api/auth/register/` — Реєстрація користувача  
- `POST /api/auth/login/` — Вхід (отримання токена)  
- `GET /api/auth/profile/` — Перегляд профілю  
- `PUT /api/auth/profile/` — Повне оновлення профілю  
- `PATCH /api/auth/profile/` — Часткове оновлення профілю  
- `GET /api/chats/` — Список чатів поточного користувача  
- `GET /api/chats/{id}/` — Деталі чату  
- `GET /api/messages/?chat={id}` — Список повідомлень у чаті (кореневі, з відповідями)  
- `POST /api/messages/` — Надсилання повідомлення  
- `GET /api/messages/{id}/` — Деталі повідомлення  
- `PUT /api/messages/{id}/` — Повне оновлення повідомлення  
- `PATCH /api/messages/{id}/` — Часткове оновлення повідомлення  
- `DELETE /api/messages/{id}/` — Видалення повідомлення   
- `GET /api/info/` — Інформація про додаток  
- `GET /api/schema/` — OpenAPI-схема (YAML/JSON)  
- `GET /api/docs/` — Документація в браузері (ReDoc)  

## Технології
* **Python** 3.14.2  
* **Django** 5.2.7  
* **Django REST Framework** 3.15.2  
* **drf-spectacular** 0.28.0  
* **django-cors-headers** 4.6.0  
* **SQLite** (база даних)  
