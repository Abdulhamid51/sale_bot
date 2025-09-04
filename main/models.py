from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

TARIF_TYPES = {
    "like": "156", # Лайков
    "coverage": "106", # Охват
    "views": "5", # Просмотров
    "saved": "99", # Сохраненные
    "repost": "147", # Репост
    "jap_views1": "793", # Просмотров
    "jap_views2": "442", # Просмотров
}

# Unregister the original User model
admin.site.unregister(User)

# Extend UserAdmin to add custom fields
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'password', 'is_active', 'is_staff', 'is_superuser')}),
    )

class Tarif(models.Model):
    name = models.CharField("Название тарифа", max_length=250)
    like = models.IntegerField("Лайков", default=0)
    like_speed = models.IntegerField("Скорость. Лайков", default=0)
    coverage = models.IntegerField("Охват", default=0)
    coverage_speed = models.IntegerField("Скорость. Охват", default=0)
    saved = models.IntegerField("Сохраненные", default=0)
    saved_speed = models.IntegerField("Скорость. Сохраненные", default=0)
    views = models.IntegerField("Просмотров", default=0)
    jap_quantity = models.IntegerField("Quantity JAP", default=0)
    jap_runs = models.IntegerField("Runs JAP", default=0)
    jap_interval = models.IntegerField("Interval (in minutes) JAP", default=0)
    repost = models.IntegerField("Репост", default=0)
    repost_speed = models.IntegerField("Скорость. Репост", default=0)

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tarif = models.ForeignKey(Tarif, on_delete=models.SET_NULL, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    orders = models.TextField(blank=True, null=True)
    jap_orders = models.TextField(blank=True, null=True)
    for_test = models.BooleanField(default=False)
    publication = models.IntegerField("Публикаций", default=0)
    finished = models.BooleanField(default=False)

    @property
    def count_orders(self):
        orders = self.orders.split(',') if self.orders else ','
        return orders.__len__()-1

    @property
    def count_jap_orders(self):
        orders = self.jap_orders.split(',') if self.jap_orders else ','
        return orders.__len__()-1

    def __str__(self):
        return self.tarif.name if self.tarif else f'{self.date}'


class ApiKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь", blank=True, null=True)
    key = models.TextField("venro.ru")
    jap_key = models.TextField("justanotherpanel.com", blank=True, null=True)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = "API-ключ"
        verbose_name_plural = "API-ключи"