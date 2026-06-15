from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('favorites/toggle/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('recipe/add/', views.recipe_add, name='recipe_add'),
]