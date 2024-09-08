# Generated by Django 5.1 on 2024-09-08 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category_name",
                    models.CharField(
                        help_text="Введите наименование категории",
                        max_length=50,
                        verbose_name="Наименование категории",
                    ),
                ),
                (
                    "category_description",
                    models.TextField(
                        help_text="Опишите категорию", verbose_name="Описание категории"
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "product_name",
                    models.CharField(
                        help_text="Введите наименование продукта",
                        max_length=50,
                        verbose_name="Наименование продукта",
                    ),
                ),
                (
                    "product_description",
                    models.TextField(
                        help_text="Опишите продукт",
                        max_length=500,
                        verbose_name="Описание продукта ",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение продукта",
                        null=True,
                        upload_to="products/",
                        verbose_name="Изображение продукта",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Введите стоимость продукта",
                        max_digits=10,
                        verbose_name="Стоимость продукта",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="catalog.category",
                        verbose_name="Принадлежит категории",
                    ),
                ),
            ],
            options={
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
                "ordering": ["product_name", "product_description", "price"],
            },
        ),
    ]