from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Назва')
    slug = models.SlugField(max_length=120, unique=True, blank=True, allow_unicode=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE, verbose_name='Категорія'
    )
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(max_length=220, unique=True, blank=True, allow_unicode=True)
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна, ₴')
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True, null=True, verbose_name='Фото')
    available = models.BooleanField(default=True, verbose_name='У наявності')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', args=[self.slug])

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Нове'),
        (STATUS_CONFIRMED, 'Підтверджено'),
        (STATUS_DONE, 'Виконано'),
        (STATUS_CANCELLED, 'Скасовано'),
    ]

    full_name = models.CharField(max_length=150, verbose_name="ПІБ")
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.CharField(max_length=250, blank=True, verbose_name='Адреса доставки')
    comment = models.TextField(blank=True, verbose_name='Коментар до замовлення')
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'Замовлення №{self.id} ({self.full_name})'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.SET_NULL, null=True, verbose_name='Товар'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна на момент замовлення')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.product} x {self.quantity}'
