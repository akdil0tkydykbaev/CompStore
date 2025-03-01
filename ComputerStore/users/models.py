from django.db import models
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь",
                                related_name="profile")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.user.username
