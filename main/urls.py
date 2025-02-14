from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', create_order_page, name='create_order_page'),
    path('create_order/', create_order, name='create_order'),
    path('tarif_component/<int:id>/', tarif_component, name='tarif_component'),
    path('check_telegram_user/<str:tg_id>', check_telegram_user, name='check_telegram_user'),
    path('orders/', orders, name='orders'),
    path('test_orders/', test_orders, name='test_orders'),
    path('delete_order/', delete_order, name='delete_order'),
]