from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['category', 'title', 'description', 'ingredients', 'time_minutes', 'difficulty', 'image']
        
        # ДОБАВЬТЕ ЭТОТ СЛОВАРЬ ДЛЯ ПЕРЕВОДА:
        labels = {
            'category': 'Категория блюда',
            'title': 'Название рецепта',
            'description': 'Способ приготовления (описание)',
            'ingredients': 'Ингредиенты',
            'time_minutes': 'Время приготовления (в минутах)',
            'difficulty': 'Сложность',
            'image': 'Иллюстрация (фото блюда)',
        }
        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Например: Бабушкины блинчики'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Опишите пошагово процесс приготовления...'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Мука — 200г\nМолоко — 500мл\nЯйца — 2 шт.'}),
            'time_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'difficulty': forms.Select(attrs={'class': 'form-input'}),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
        }