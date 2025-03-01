from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('installment', 'Оформить в рассрочку'),
        ('cash', 'Оплата наличными'),
        ('transfer', 'Перевод по номеру'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь")
    cart = models.ForeignKey('cart.Cart', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Корзина заказа")
    full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Полное имя")
    email = models.EmailField(null=True, blank=True, verbose_name="E-mail")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    delivery_method = models.CharField(max_length=100, choices=[('delivery', 'Доставка по Кыргызстану'), ('pickup', 'Самовывоз')], verbose_name="Метод доставки")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий к заказу")
    consent = models.BooleanField(default=False, verbose_name="Согласие на обработку персональных данных")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='processing', verbose_name="Статус")
    # total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Всего к оплате", blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")
    address = models.TextField(verbose_name="Адрес доставки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True, verbose_name="Чек")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Всего к оплате", blank=True, null=True)

    def save(self, *args, **kwargs):
        """Пересчитываем сумму перед сохранением"""
        if self.pk:
            self.total_amount = sum(item.total_price for item in self.items.all())
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Soft-delete: помечаем заказ как удаленный."""
        self.is_deleted = True
        self.save()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ {self.id} от {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

