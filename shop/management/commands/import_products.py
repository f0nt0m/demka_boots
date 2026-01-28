import csv

from django.core.management.base import BaseCommand

from shop.models import Category, Manufacturer, Product, Supplier


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]

        try:
            with open(file_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=";")

                count = 0
                for row in reader:
                    if not row.get("Артикул") or not row.get("Артикул").strip():
                        continue

                    category, _ = Category.objects.get_or_create(
                        name=row["Категория товара"]
                    )

                    manufacturer, _ = Manufacturer.objects.get_or_create(
                        name=row["Производитель"]
                    )

                    supplier, _ = Supplier.objects.get_or_create(name=row["Поставщик"])

                    Product.objects.update_or_create(
                        article=row["Артикул"],
                        defaults={
                            "name": row["Наименование товара"],
                            "unit": row["Единица измерения"],
                            "price": row["Цена"],
                            "supplier": supplier,
                            "manufacturer": manufacturer,
                            "category": category,
                            "discount": int(row.get("Действующая скидка") or 0),
                            "stock_quantity": int(row.get("Кол-во на складе") or 0),
                            "description": row.get("Описание товара", ""),
                            "photo": row.get("Фото", ""),
                        },
                    )
                    count += 1

                self.stdout.write(self.style.SUCCESS(f"Импортировано товаров: {count}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Файл не найден"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
