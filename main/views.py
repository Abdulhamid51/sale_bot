from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
import requests

def venro_order_create(key, service_id, link, count, speed, posts):
    url = 'https://venro.ru/api/orders'
    data = {
        'action': 'add',
        'key': key,
        'url': link,
        'count': count,
        'type': service_id
    }
    if posts != 'off':
        data['posts'] = posts
    if speed > 0:
        data['speed'] = speed
    response = requests.post(url, data=data)
    print(response.json())
    if response.json().get('id'):
        return response.json()
    else:
        return False
    
def venro_order_delete(key, orders):
    url = 'https://venro.ru/api/orders'
    data = {
        'action': 'cancel',
        'key': key,
        'orders': orders
    }
    response = requests.post(url, data=data)
    print(response.json())
    
def venro_order_check(order_id):
    url = 'https://venro.ru/api/orders'
    data = {
        'action': 'check',
        'key': ApiKey.objects.last().key,
        'id': order_id
    }
    response = requests.post(url, data=data)
    if response.json().get('url'):
        return response.json()
    else:
        return False

def create_order_page(request):
    tarifs = Tarif.objects.all()
    clients = Client.objects.all()
    context = {
        'tarifs': tarifs,
        'clients': clients
    }
    return render(request, 'index.html', context)

def create_order(request):
    try:
        telegram_id = request.POST.get('telegram_id')
        user = User.objects.filter(last_name=telegram_id).last()
        if not user:
            messages.error(request, 'User not found !')
            return redirect('main:create_order_page')
        key = ApiKey.objects.filter(user=user).last()
        if not key:
            messages.error(request, 'Venro error !')
            return redirect('main:create_order_page')
        tarif_id = request.POST.get('tarif_id')
        client_id = request.POST.get('client_id')
        link = request.POST.get('link')
        publication = request.POST.get('publication')
        test = True if request.POST.get('test') else False
        if user.is_staff == False:
            test = True
            publication = 'off'
        tarif = Tarif.objects.get(id=tarif_id)
        if client_id:
            client = Client.objects.get(id=client_id)
        else:
            client = None

        orders = ''

        if publication == 'on':
            publication = tarif.publication
        else:
            publication = 'off'

        if tarif.like > 0:
            vo = venro_order_create(
                key=key,
                service_id=TARIF_TYPES['like'],
                link=link,
                count=tarif.like,
                speed=tarif.like_speed,
                posts=publication
            )
            if vo != False:
                orders += f"{vo['id']},"

                
        if tarif.coverage > 0:
            vo = venro_order_create(
                key=key,
                service_id=TARIF_TYPES['coverage'],
                link=link,
                count=tarif.coverage,
                speed=tarif.coverage_speed,
                posts=publication
            )
            if vo != False:
                orders += f"{vo['id']},"
                
        if tarif.saved > 0:
            vo = venro_order_create(
                key=key,
                service_id=TARIF_TYPES['saved'],
                link=link,
                count=tarif.saved,
                speed=tarif.saved_speed,
                posts=publication
            )
            if vo != False:
                orders += f"{vo['id']},"

        if tarif.views > 0:
            vo = venro_order_create(
                key=key,
                service_id=TARIF_TYPES['views'],
                link=link,
                count=tarif.views,
                speed=0,
                posts=publication
            )
            if vo != False:
                orders += f"{vo['id']},"
                
        Order.objects.create(
            tarif=tarif,
            client=client,
            orders=orders,
            for_test=test
        )
        messages.success(request, 'Заказы созданы')
        return redirect('main:create_order_page')
    except Exception as error:
        messages.error(request, f'Error: {error}')
        return redirect('main:create_order_page')

def tarif_component(request, id):
    tarif = Tarif.objects.get(id=id)
    return render(request, 'tarif_component.html', {'tarif': tarif})

def check_telegram_user(request, tg_id):
    user = User.objects.filter(last_name=tg_id)
    if user:
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
    
def orders(request):
    orders = Order.objects.filter(for_test=False)
    return render(request, 'orders.html', {'orders': orders})
    
def test_orders(request):
    orders = Order.objects.filter(for_test=True)
    return render(request, 'tests.html', {'orders': orders})

def delete_order(request):
    tg_id = request.GET.get('tg_id')
    order_id = request.GET.get('order_id')
    user = User.objects.filter(last_name=tg_id).last()
    if not user:
        messages.error(request, 'User not found !')
        return redirect(request.META.get('HTTP_REFERER', '/app/'))
    order = Order.objects.get(id=order_id)
    if order.for_test == False and user.is_staff == False:
        messages.error(request, 'Only admin can delete !')
        return redirect(request.META.get('HTTP_REFERER', '/app/'))
    key = ApiKey.objects.filter(user=user).last()
    if not key:
        messages.error(request, 'Venro error !')
        return redirect(request.META.get('HTTP_REFERER', '/app/'))
    venro_order_delete(key, order.orders)
    order.delete()
    messages.success(request, 'Заказ отменен')
    return redirect(request.META.get('HTTP_REFERER', '/app/'))
