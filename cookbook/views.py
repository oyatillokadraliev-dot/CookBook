from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q # Импортируем Q для сложного поиска по нескольким словам
from .models import Recipe, Category
from .forms import RecipeForm

def get_fav_count(request):
    """Вспомогательная функция для подсчета избранного в сессии"""
    return len(request.session.get('favorites', []))

def recipe_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort', '-id')
    
    recipes = Recipe.objects.all()
    
    # 1. Фильтрация по категориям
    if category_id:
        recipes = recipes.filter(category_id=category_id)
        
    # 2. Умный поиск по отдельным словам (находит «суп-пюре» по запросу «суп»)
    if search_query:
        words = search_query.split()
        query_filter = Q()
        for word in words:
            query_filter |= Q(title__icontains=word)
        recipes = recipes.filter(query_filter)
        
    # 3. Сортировка выдачи
    if sort_by == 'time':
        recipes = recipes.order_by('time_minutes')
    elif sort_by == 'difficulty':
        recipes = recipes.order_by('difficulty')
    else:
        recipes = recipes.order_by('-id') # Сначала новые
        
    # 4. Пагинация (Выводим строго по 6 рецептов на страницу)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, 'cookbook/list.html', {
        'recipes': page_obj, # Передаем объект страницы с рецептами
        'category': Category.objects.all(),
        'current_category': category_id,
        'search_query': search_query,
        'current_sort': sort_by,
        'fav_count': get_fav_count(request)
    })

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    # Похожие рецепты (из той же категории, исключая текущий, лимит 3 штуки)
    similar_recipes = Recipe.objects.filter(category=recipe.category).exclude(pk=recipe.pk)[:3]
    
    return render(request, 'cookbook/detali.html', {
        'recipe': recipe,
        'similar_recipes': similar_recipes,
        'fav_count': get_fav_count(request)
    })

def favorites_list(request):
    fav_ids = request.session.get('favorites', [])
    recipes = Recipe.objects.filter(id__in=fav_ids)
    return render(request, 'cookbook/favorites.html', {
        'recipes': recipes,
        'fav_count': len(fav_ids)
    })

def toggle_favorite(request, pk):
    favorites = request.session.get('favorites', [])
    if pk in favorites:
        favorites.remove(pk)
    else:
        favorites.append(pk)
    request.session['favorites'] = favorites
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'recipe_list'))

def recipe_add(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()
        
    return render(request, 'cookbook/recipe_form.html', {
        'form': form,
        'fav_count': get_fav_count(request)
    })