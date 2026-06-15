from django.contrib import admin
from .models import Category, Recipe

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'time_minutes', 'difficulty']
    list_filter =  ['category' , 'difficulty']
    search_fields = ['title', 'difficulty']