from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

TARIF_TYPES = {
    "like": "105", # Лайков
    "coverage": "106", # Охват
    "views": "5", # Просмотров
    "saves": "99", # Сохраненные
}

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
    like = models.IntegerField("Лайков", default=0)
    coverage = models.IntegerField("Охват", default=0)
    saved = models.IntegerField("Сохраненные", default=0)
    views = models.IntegerField("Просмотров", default=0)
    publication = models.IntegerField("Публикаций", default=0)
    speed = models.IntegerField("Скорость", default=0)

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
    

class Order(models.Model):
    order_id = models.CharField(max_length=200)
    service_id = models.CharField(max_length=20)
    url = models.CharField(max_length=1000)
    count = models.CharField(max_length=200)
    remains = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    charge = models.CharField(max_length=200)
    
    def __str__(self):
        return self.order_id