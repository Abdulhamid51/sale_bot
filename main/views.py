from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
import requests

def jap_order_create(key, service_id, link, count, posts, loop_count):
    loop_minutes = [10, 15, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 360, 420, 480, 540, 600]
    posts = 0 if posts == 'off' else posts
    url = 'https://justanotherpanel.com/api/v2'
    orders = ''
    for i in loop_minutes[:loop_count]:
        data = {
            'action': 'add',
            'key': key,
            'service': service_id,
            'username': link,
            'min': count, # count of views
            'max': count, # count of views
            'posts': posts,
            'delay': i
        }
        response = requests.post(url, data=data)
        print(response.json())
        order_id = response.json().get('order')
        if order_id:
            orders += f'{order_id},'
    print(orders)
    return orders

def jap_default_order_create(key, service_id, link, quantity, runs, interval):
    url = 'https://justanotherpanel.com/api/v2'
    orders = ''
    data = {
        'action': 'add',
        'key': key,
        'service': service_id,
        'link': link,
        'quantity': quantity,
        'runs': runs,
        'interval': interval
    }
    response = requests.post(url, data=data)
    print(response.json())
    order_id = response.json().get('order')
    if order_id:
        orders += f'{order_id},'
    return orders

def jap_order_delete(key, orders):
    url = 'https://justanotherpanel.com/api/v2'
    print(orders)
    data = {
        'action': 'cancel',
        'key': key,
        'orders': orders
    }
    response = requests.post(url, data=data)
    print(response.json())

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
    
def venro_orders_check(key, orders):
    url = 'https://venro.ru/api/orders'
    data = {
        'action': 'check',
        'key': key,
        'orders': orders
    }
    response = requests.post(url, data=data)
    if response.json():
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
        jap_key = ''
        if not key:
            messages.error(request, 'Venro error !')
            return redirect('main:create_order_page')
        else:
            jap_key = key.jap_key
            key = key.key

        tarif_id = request.POST.get('tarif_id')
        client_id = request.POST.get('client_id')
        link = request.POST.get('link')
        publication = request.POST.get('publication')
        publication_count = request.POST.get('publication_count')
        views_count = int(request.POST.get('views_count')) if request.POST.get('views_count') else 0
        views_loop = int(request.POST.get('views_loop')) if request.POST.get('views_loop') else 0

        if views_loop > 17:
            messages.error(request, 'Views loop is more than 17 !')
            return redirect('main:create_order_page')

        if publication == 'on':
            publication = publication_count
            test = False
        else:
            publication = 'off'
            test = True

        if user.is_staff == False:
            publication = 'off'
            test = True

        tarif = Tarif.objects.get(id=tarif_id)

        if client_id:
            client = Client.objects.get(id=client_id)
        else:
            client = None

        orders = ''
        jap_orders = ''

        if tarif.like > 0:
            vo = venro_order_create(
                key=key,
                service_id=TarifCodes.objects.last().like, #TARIF_TYPES['like'],
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
                service_id=TarifCodes.objects.last().coverage, #TARIF_TYPES['coverage'],
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
                service_id=TarifCodes.objects.last().saved, #TARIF_TYPES['saved'],
                link=link,
                count=tarif.saved,
                speed=tarif.saved_speed,
                posts=publication
            )
            if vo != False:
                orders += f"{vo['id']},"
                
        if tarif.repost > 0:
            vo = venro_order_create(
                key=key,
                service_id=TarifCodes.objects.last().repost, #TARIF_TYPES['repost'],
                link=link,
                count=tarif.repost,
                speed=tarif.repost_speed,
                posts=publication
            )
            if vo != False:
                orders += f"{vo['id']},"
        
        if tarif.views > 0:
            vo = venro_order_create(
                key=key,
                service_id=TarifCodes.objects.last().views, #TARIF_TYPES['views'],
                link=link,
                count=tarif.views,
                speed=0,
                posts=publication
            )
            if vo != False:
                orders += f"{vo['id']},"
        
        if tarif.views_2 > 0:
            vo = venro_order_create(
                key=key,
                service_id=TarifCodes.objects.last().views_2, #TARIF_TYPES['views'],
                link=link,
                count=tarif.views_2,
                speed=tarif.views_2_speed,
                posts=publication
            )
            if vo != False:
                orders += f"{vo['id']},"

        if publication != 'off':
            if views_count and views_loop > 0:
                jo = jap_order_create(
                    key=jap_key,
                    service_id=TarifCodes.objects.last().jap_views1, #TARIF_TYPES['jap_views1'],
                    link=link,
                    count=views_count,
                    loop_count=views_loop,
                    posts=publication
                )
                jap_orders = jo
        else:
            if tarif.jap_quantity > 0:
                jo = jap_default_order_create(
                    key=jap_key,
                    service_id=TarifCodes.objects.last().jap_views2, #TARIF_TYPES['jap_views2'],
                    link=link,
                    quantity=tarif.jap_quantity,
                    runs=tarif.jap_runs,
                    interval=tarif.jap_interval
                )
                jap_orders = jo
                
        Order.objects.create(
            user=user,
            tarif=tarif,
            link=link,
            client=client,
            orders=orders,
            jap_orders=jap_orders,
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
        return JsonResponse({'success': True, 'is_staff': user.last().is_staff})
    else:
        return JsonResponse({'success': False})
    
def orders(request):
    orders = Order.objects.filter(for_test=False).order_by('-id')[:100]
    return render(request, 'orders.html', {'orders': orders})
    
def test_orders(request):
    orders = Order.objects.filter(for_test=True).order_by('-id')[:100]
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
    jap_key = key.jap_key
    venro_order_delete(key, order.orders)
    jap_order_delete(jap_key, order.jap_orders)
    order.delete()
    messages.success(request, 'Заказ отменен')
    return redirect(request.META.get('HTTP_REFERER', '/app/'))


# from .cronjobs import finished_orders_send
# finished_orders_send()
