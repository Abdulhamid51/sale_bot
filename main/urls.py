from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', create_order_page, name='create_order_page'),
    path('create_order/', create_order, name='create_order'),
    path('tarif_component/<int:id>/', tarif_component, name='tarif_component'),
]