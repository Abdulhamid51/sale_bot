from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Unregister the original User model
admin.site.unregister(User)

# Extend UserAdmin to add custom fields
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'password', 'is_active', 'is_staff')}),
    )

class Tarif(models.Model):
    name = models.CharField("Название тарифа", max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ['name']

class Client(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    tarif = models.ForeignKey(Tarif, verbose_name="Тариф", on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField("Имя", max_length=250)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    created_date = models.DateField("Дата создания", auto_now_add=True)
    payment_date = models.DateField("Дата платежа", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['name']

    @property
    def is_active(self):
        if self.payment_date:
            return self.payment_date >= timezone.now().date()
        return False