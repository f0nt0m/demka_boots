# Магазин обуви

Django-проект для демоэкзамена.

## Что реализовано

- Модели данных: Product, Category, Manufacturer, Supplier
- Команда импорта товаров из CSV

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install django
python manage.py migrate
python manage.py import_products import_data/Tovar.csv
python manage.py runserver
```
