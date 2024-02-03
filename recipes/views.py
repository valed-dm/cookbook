# import pandas as pd
from django.db import transaction
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Ingredient, Qty, Recipe, RecipeIngredient, Unit


class IndexView(generic.ListView):
    """Renders the all recipes page to 5 latest"""
    template_name = "recipes/index.html"
    context_object_name = "latest_recipes_list"

    def get_queryset(self):
        """Return the last five published recipes (not including those set to be
        published in the future)."""

        return Recipe.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class RecipeIngredientsView(generic.ListView):
    """Render recipe ingredients"""
    model = RecipeIngredient
    template_name = "recipes/detail.html"
    extra_context = {"recipe_title": "RECIPE TITLE"}

    def get_queryset(self):
        """
        Shows recipe's ingredient list.
        """
        pk = self.kwargs.get("pk")
        # db request optimization with select_related()
        ingredients = RecipeIngredient.objects.select_related().filter(recipe_id=pk).order_by("ingredient__name")
        recipe = Recipe.objects.get(id=pk)
        self.extra_context["recipe_title"] = recipe.title.upper()

        return ingredients


def add_product_to_recipe(request, recipe_id, product_id, weight, measure_unit):
    """Adds new product to recipe. If recipe contains the product it's weight is altered.
    Validates data given on a presence in db.
    """
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
    except Recipe.DoesNotExist:
        return render(
            request,
            "recipes/detail.html",
            {
                "recipe_title": "RECIPE DOES NOT EXIST",
                "error_message": f"recipe with id {recipe_id} is not found in the database",
            },
        )

    # recipe = get_object_or_404(Recipe, id=recipe_id)

    try:
        ingredient = Ingredient.objects.get(pk=product_id)
    except Ingredient.DoesNotExist:
        return render(
            request,
            "recipes/detail.html",
            {
                "recipe_title": f"{recipe.title.upper()}: upgrade is not possible",
                "error_message": f"ingredient with id {product_id} is not found in the database",
            },
        )

    try:
        qty = Qty.objects.get(amount=weight)
    except Qty.DoesNotExist:
        return render(
            request,
            "recipes/detail.html",
            {
                "recipe_title": f"{recipe.title.upper()}: upgrade is not possible",
                "error_message": f"weight value {weight} is not found in the database",
            },
        )

    try:
        unit = Unit.objects.get(unit=measure_unit)
    except Unit.DoesNotExist:
        return render(
            request,
            "recipes/detail.html",
            {
                "recipe_title": f"{recipe.title.upper()}: upgrade is not possible",
                "error_message": f"unit measure {measure_unit} is not found in the database",
            },
        )

    try:
        q = Q(recipe=recipe) & Q(ingredient=ingredient)
        # solving race condition with select_for_update()
        with transaction.atomic():
            recipe_ingredient = RecipeIngredient.objects.select_for_update().get(q)
            recipe_ingredient.qty = qty
            recipe_ingredient.unit = unit
            recipe_ingredient.save()
    except RecipeIngredient.DoesNotExist:
        new_recipe_ingredient = RecipeIngredient(
            recipe=recipe,
            unit=unit,
            qty=qty,
            ingredient=ingredient
        )
        new_recipe_ingredient.save()

    return HttpResponseRedirect(reverse("recipes:detail", args=(recipe_id,)))


def cook_recipe(request, recipe_id):
    """Increments by 1 for all recipe's ingredients"""
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    with transaction.atomic():
        for ing in ingredients:
            "'F' expression avoids retrieving the 'times_used' value from the database into Python memory."
            "It performs the increment operation directly at the database level"
            Ingredient.objects.filter(id=ing.ingredient.id).update(times_used=F("times_used") + 1)
    # ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    # products_for_bulk_update = []
    # for ing in ingredients:
    #     product = Ingredient.objects.get(id=ing.ingredient.id)
    #     product.times_used = F("times_used") + 1
    #     products_for_bulk_update.append(product)
    # Ingredient.objects.bulk_update(products_for_bulk_update, ["times_used"])

    return HttpResponseRedirect(reverse("recipes:detail", args=(recipe_id,)))


def show_recipes_without_product(request, product_id):
    """Shows recipes with product absence or amount less than 10g"""
    q = Q(ingredient_id=product_id) & Q(qty__amount__gte=10) & Q(unit__unit="g")
    positive_query = (
        RecipeIngredient.objects
        .select_related("recipe", "unit", "qty", "ingredient")
        .filter(q)
    )

    recipes_with_product_ids = []
    for obj in positive_query:
        recipes_with_product_ids.append(obj.recipe.id)

    q = Q(id__in=recipes_with_product_ids)
    negative_query_recipes = Recipe.objects.filter(~q)

    # q = Q(recipe_id__in=recipes_with_product_ids)
    # negative_query_recipe_ingredients = (
    #     RecipeIngredient.objects
    #     .select_related("recipe", "unit", "qty", "ingredient")
    #     .filter(~q)  # search for recipes without product
    #     .order_by("recipe__title", "ingredient__name")
    # )
    #
    # recipes_with_product_absence = []
    # for obj in negative_query_recipe_ingredients:
    #     recipes_with_product_absence.append(
    #         {
    #             "recipe": obj.recipe.title,
    #             "ingredient": obj.ingredient.name,
    #             "qty": obj.qty.amount,
    #             "unit": obj.unit.unit,
    #         },
    #     )
    # df = pd.DataFrame(recipes_with_product_absence)
    # print(df)

    return render(
        request,
        "recipes/without_product.html",
        {"recipes": negative_query_recipes}
    )
