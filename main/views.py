from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import requests

def venro_order_create(service_id)

def create_order_page(request):
    tarifs = Tarif.objects.all()
    context = {
        'tarifs': tarifs
    }
    return render(request, 'index.html', context)

def create_order(request):
    try:
        tarif_id = request.POST.get('tarif_id')
        link = request.POST.get('link')
        publication = request.POST.get('publication')
        test = True if request.POST.get('test') else False

        tarif = Tarif.objects.get(id=tarif_id)
        if publication == 'on':
            publication = tarif.publication
        else:
            publication = 'off'
        if tarif.like > 0:
            Order.objects.create(
                order_id='652888027',
                service_id=TARIF_TYPES['like'],
                url=link,
                count=str(tarif.like),
                remains=str(tarif.like),
                status='Completed',
                for_test=test,
                charge='0.005',
                publication=str(publication)
            )
        if tarif.coverage > 0:
            Order.objects.create(
                order_id='652888027',
                service_id=TARIF_TYPES['coverage'],
                url=link,
                count=str(tarif.coverage),
                remains=str(tarif.coverage),
                status='Completed',
                for_test=test,
                charge='0.005',
                publication=str(publication)
            )
        if tarif.saved > 0:
            Order.objects.create(
                order_id='652888027',
                service_id=TARIF_TYPES['saved'],
                url=link,
                count=str(tarif.saved),
                remains=str(tarif.saved),
                status='Completed',
                for_test=test,
                charge='0.005',
                publication=str(publication)
            )
        if tarif.views > 0:
            Order.objects.create(
                order_id='652888027',
                service_id=TARIF_TYPES['views'],
                url=link,
                count=str(tarif.views),
                remains=str(tarif.views),
                status='Completed',
                for_test=test,
                charge='0.005',
                publication=str(publication)
            )

        messages.success(request, 'Заказы созданы')
        return redirect('main:create_order_page')
    except Exception as error:
        messages.error(request, f'Error: {error}')
        return redirect('main:create_order_page')

def tarif_component(request, id):
    tarif = Tarif.objects.get(id=id)
    return render(request, 'tarif_component.html', {'tarif': tarif})