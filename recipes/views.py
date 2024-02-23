from django.http import Http404, HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404

from utils.recipes.factory import make_recipe
from .models import Recipe

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        #'recipes': [make_recipe() for _ in range(10)],
        'recipes': recipes,
        
    })

def category(request, category_id):
    #recipes = Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')

    #get_attr
    #category_name = getattr(getattr(recipes.first(), 'category', None), 'name', 'Not found')

    #2 formas de dar resposta 404
    #f not recipes: 
        #return HttpResponse(content='Not Found', status=404)
        #raise Http404('Not found')
    
    #return render(request, 'recipes/pages/category.html', context={
    #    'recipes': recipes,
    #    'title': f'Categoria - {recipes.first().category.name}'
        
    #})


    #get_list_or_404 retorna uma lista, como parâmetro passamos a classe e os filtros
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))
    
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'Categoria - {recipes[0].category.name}'
        
    })

def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })