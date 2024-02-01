import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Recipe(models.Model):
    """Contains information about a recipe"""
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.title

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.pub_date <= now


class Unit(models.Model):
    """Contains information about measure units"""
    unit = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.unit


class Qty(models.Model):
    """Available qty values for a recipe"""
    amount = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.amount)


class Ingredient(models.Model):
    """Available ingredients for a recipe"""
    name = models.CharField(max_length=200, unique=True)
    times_used = models.IntegerField(default=0)

    def __str__(self):
        info = f"{self.name}"
        return info


class RecipeIngredient(models.Model):
    """Recipe ingredients table"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    qty = models.ForeignKey(Qty, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        ingredient = f"{self.recipe}-{self.ingredient}: {self.qty}{self.unit}"
        return ingredient

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'ingredient'], name='unique_recipe_ingredient')
        ]
