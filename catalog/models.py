from django.db import models
from django.db.models import SET_NULL

from users.models import User


class Category(models.Model):
    category_name = models.CharField(
        max_length=50,
        verbose_name="Наименование категории",
        help_text="Введите наименование категории",
    )
    category_description = models.TextField(
        verbose_name="Описание категории", help_text="Опишите категорию"
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    product_name = models.CharField(
        max_length=50,
        verbose_name="Наименование продукта",
        help_text="Введите наименование продукта",
    )
    product_description = models.TextField(
        max_length=500, verbose_name="Описание продукта ", help_text="Опишите продукт"
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Изображение продукта",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Принадлежит категории",
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость продукта",
        help_text="Введите стоимость продукта",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    owner = models.ForeignKey(User, verbose_name='владелец', help_text='укажите владельца', on_delete=SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=False, verbose_name='статус')

    def get_active_version(self):
        return self.versions.filter(version_flag=True).first()

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["product_name", "product_description", "price"]

class Version(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        verbose_name="Продукт",
        blank=True,
        null=True,
        related_name="versions",
    )
    version_number = models.IntegerField(verbose_name='номер версии')
    name = models.CharField(max_length=150, verbose_name='название версии')
    version_flag = models.BooleanField(default=False, verbose_name='признак версии')

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["product", "version_number", "name", "version_flag"]
        constraints = [
            models.UniqueConstraint(fields=['product', 'version_flag'],
                                    condition=models.Q(version_flag=True),
                                    name='unique_active_version')
        ]

    def __str__(self):
        return f'{self.name} - {self.version_number}'

    def save(self, *args, **kwargs):
        if not self.version_number:
            max_version = Version.objects.filter(product=self.product).aggregate(models.Max('version_number'))[
                'version_number__max']
            self.version_number = (max_version + 1) if max_version is not None else 1
        if self.version_flag:
            Version.objects.filter(product=self.product, version_flag=True).update(version_flag=False)
        super().save(*args, **kwargs)
