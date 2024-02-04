from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, Unit, Qty, Ingredient, RecipeIngredient


class APIFunctionsTest(TestCase):
    """Tests API endpoint functions for adding and updating recipe's product data"""

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Pancake', description='Description')
        Unit.objects.create(unit='g', description='gram, one-thousandth of a kilogram in Si')
        Qty.objects.create(amount=100),
        Qty.objects.create(amount=10)
        Ingredient.objects.create(name="sugar"),
        Ingredient.objects.create(name="salt")

        recipe = Recipe.objects.get(id=1)
        unit = Unit.objects.get(id=1)
        qty = Qty.objects.get(id=1)
        ingredient = Ingredient.objects.get(id=1)

        RecipeIngredient.objects.create(recipe=recipe, unit=unit, qty=qty, ingredient=ingredient)

    def test_add_new_product_to_recipe(self):
        """Adds new ingredient to recipe
            method GET; path=recipes/add_product/<int:recipe_id>/<int:product_id>/<str:weight>/<str:measure_unit>/"""
        response = self.client.get(reverse("recipes:add_product", args=(1, 2, 100, "g")))
        self.assertEqual(response.status_code, 302)

        ingredients = RecipeIngredient.objects.select_related().filter(recipe_id=1)
        for i in ingredients:
            self.assertEqual(len(ingredients), 2)
            self.assertIn(i.ingredient.name, ["sugar", "salt"])
            self.assertIn(i.qty.amount, [100, 100])
            self.assertEqual(i.unit.unit, "g")

    def test_alter_product_qty_in_recipe(self):
        """Updates existing ingredient qty 100 -> 10 in the recipe"""
        response = self.client.get(reverse("recipes:add_product", args=(1, 2, 10, "g")))
        self.assertEqual(response.status_code, 302)

        ingredients = RecipeIngredient.objects.select_related().filter(recipe_id=1)
        for i in ingredients:
            self.assertEqual(len(ingredients), 2)
            self.assertIn(i.ingredient.name, ["sugar", "salt"])
            self.assertIn(i.qty.amount, [10, 100])
            self.assertEqual(len(ingredients), 2)

    def test_recipe_does_not_exist(self):
        """Recipe does not exist in DB"""
        response = self.client.get(reverse("recipes:add_product", args=(2, 2, 10, "g")))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RECIPE DOES NOT EXIST")

    def test_unit_does_not_exist(self):
        """Unit does not exist in DB"""
        response = self.client.get(reverse("recipes:add_product", args=(1, 2, 10, "fg")))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "unit measure fg is not found in the database")

    def test_qty_does_not_exist(self):
        """Qty does not exist in DB"""
        response = self.client.get(reverse("recipes:add_product", args=(1, 2, 25, "g")))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "weight value 25 is not found in the database")

    def test_ingredient_does_not_exist(self):
        """Ingredient does not exist in DB"""
        response = self.client.get(reverse("recipes:add_product", args=(1, 33, 10, "g")))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ingredient with id 33 is not found in the database")

    def test_cook_recipe(self):
        """Tests cook recipe function which increments all recipe ingredients times_used field by 1
            method GET; path="cook_recipe/<int:recipe_id>/"""
        self.client.get(reverse("recipes:add_product", args=(1, 2, 100, "g")))
        self.client.get(reverse("recipes:cook_recipe", args=(1,)))
        ingredients = RecipeIngredient.objects.select_related().all()
        for i in ingredients:
            self.assertEqual(i.ingredient.times_used, 1)

    def test_show_recipes_without_product(self):
        Recipe.objects.create(title='Apple Pie')
        Recipe.objects.create(title='Stewed Pork')
        Ingredient.objects.create(name="flour")
        Ingredient.objects.create(name="pork")
        self.client.get(reverse("recipes:add_product", args=(2, 3, 100, "g")))
        self.client.get(reverse("recipes:add_product", args=(3, 4, 100, "g")))
        response = self.client.get(reverse("recipes:without_product", args=(1,)))
        self.assertContains(response, "Apple Pie")
        self.assertContains(response, "Stewed Pork")
        response = self.client.get(reverse("recipes:without_product", args=(4,)))
        self.assertContains(response, "Pancake")
