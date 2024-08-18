from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

admin.site.site_header = _("Администрирование")
admin.site.site_title = _("Администрирование")
admin.site.index_title = _("")

@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'tarif', 'is_active_display', 'payment_date', 'user', 'phone', 'created_date')
    list_filter = ('user', 'tarif')
    search_fields = ('name',)

    @admin.display(description='Оплачено')
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">&#x2714;</span>')
        else:
            return format_html('<span style="color: red;">&#x2718;</span>')

admin.site.unregister(Group)
