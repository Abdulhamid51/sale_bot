from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Client(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    name = models.CharField("Имя", max_length=250)
    phone = models.CharField("Телефон", max_length=20, blank=True, null=True)
    created_date = models.DateField("Дата создания", auto_now_add=True)
    payment_date = models.DateField("Дата платежа", blank=True, null=True)
    # instagram = models.CharField("Инстаграм", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['name']

    @property
    def is_active(self):
        if self.payment_date:
            return self.payment_date >= timezone.now().date()
        return False