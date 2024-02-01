from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, Unit, Qty, Ingredient, RecipeIngredient


class RecipeListIndexViewTest(TestCase):
    """Recipes list index view tests"""

    @classmethod
    def setUpTestData(cls):
        recipes_qty = 7

        for num in range(recipes_qty):
            Recipe.objects.create(
                title=f'Pancake {num}',
                description=f'Description {num}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("recipes:index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/index.html')

    def test_recipes_qty_shown_is_five(self):
        """Test that 5 recipes are displayed though 7 exist"""
        response = self.client.get(reverse('recipes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['latest_recipes_list']), 5)


class RecipeIngredientsListViewTest(TestCase):
    """Recipe's ingredients list view tests'"""

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Pancake', description='Description')
        Unit.objects.create(unit='g', description='gram, one-thousandth of a kilogram in Si')
        Qty.objects.create(amount=100)
        Ingredient.objects.create(name="sugar")

        recipe = Recipe.objects.get(id=1)
        unit = Unit.objects.get(id=1)
        qty = Qty.objects.get(id=1)
        ingredient = Ingredient.objects.get(id=1)

        RecipeIngredient.objects.create(
            recipe=recipe,
            unit=unit,
            qty=qty,
            ingredient=ingredient
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/recipes/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("recipes:detail", args=(1,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recipes:detail', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')

    def test_recipes_ingredients_qty_shown_is_one(self):
        """Test that 1 recipe ingredient is displayed"""
        response = self.client.get(reverse('recipes:detail', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['recipeingredient_list']), 1)

    def test_recipes_ingredients_has_recipe_title(self):
        """Test that recipe title is displayed in upper case"""
        response = self.client.get(reverse('recipes:detail', args=(1,)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recipe_title'], "PANCAKE")
