# Web app "libraries"

Учебный проект на языке программирования Python с использованием фреймворка Django. Цель приложения - упрощение создания заметок по различным языкам прораммирования. Структуру такой заметки можно представить в виде дерева:
- Каталог языка прораммирования
- - Фреймфорк1
  - - Тема1
    - - Запись1
    - - ...
      - Записьn
  - ...
  - Фреймворкn
  - Библиотека1
  - ...
  - Библиотекаn

## Сборка

### Предварительные требования
- Django (v. 4.2.4)
- django_mptt (v. 0.14.0)
- pytils (v. 0.4.1)
- Pillow (v. 11.3.0)

### Запуск сервера (debug - режим)

```bash
# Клонирование репозитория
git clone https://github.com/MikhelsonVladislava/libraries_web_app_public.git
cd libraries_web_app_public

# Создание базы данных
python manage.py migrate

# Создание групп пользователей
python create_groups.py

# Запуск сервера
python manage.py runserver
```

### Используемые иконки
1) Google Icons (License - https://www.apache.org/licenses/LICENSE-2.0.html)
2) Icon Park by Bytedance Inc (License - https://www.apache.org/licenses/LICENSE-2.0.html)

Даты работы над проектом: Апрель - Август 2024 года.
Примечание: Этот проект предназначен для образовательных целей.
