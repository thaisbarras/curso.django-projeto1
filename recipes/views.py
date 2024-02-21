from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'recipes/home.html', context={
        'name': 'Thaís Barras'
    })


def contato(request):
    return HttpResponse('recipes/contato')


def sobre(request):
    return HttpResponse('recipes/sobre')