from tkinter.constants import CASCADE

from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField(help_text='Каждый ингридиент с новой строки')
    time_minutes = models.PositiveIntegerField(default=30)
    difficulty = models.CharField(max_length=20, choices=[('easy', 'легко'), ('medium', 'средне'), ('hard', 'сложно')])
    image = models.ImageField(upload_to='recipes/', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ['-created']

    def __str__(self):
        return self.title