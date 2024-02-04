from django.test import TestCase

from recipes.models import Recipe, Unit, Qty, Ingredient, RecipeIngredient


class RecipeModelTest(TestCase):
    """Recipe model's test cases."""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Recipe.objects.create(title='test_pie', description='apple_pie')

    def test_title_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_description_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_pub_date_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('pub_date').verbose_name
        self.assertEqual(field_label, 'date published')

    def test_title_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_title(self):
        recipe = Recipe.objects.get(id=1)
        expected_object_name = f'{recipe.title}'
        self.assertEqual(str(recipe), expected_object_name)

    def test_recipe_description_value(self):
        recipe = Recipe.objects.get(id=1)
        description = recipe.description
        self.assertEqual(description, 'apple_pie')


class UnitModelTest(TestCase):
    """Unit model's test cases."""

    @classmethod
    def setUpTestData(cls):
        Unit.objects.create(unit='g', description='gram, one-thousandth of a kilogram in Si')

    def test_unit_label(self):
        unit = Unit.objects.get(id=1)
        field_label = unit._meta.get_field('unit').verbose_name
        self.assertEqual(field_label, 'unit')

    def test_description_label(self):
        unit = Unit.objects.get(id=1)
        field_label = unit._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_unit_max_length(self):
        unit = Unit.objects.get(id=1)
        max_length = unit._meta.get_field('unit').max_length
        self.assertEqual(max_length, 10)

    def test_unit_description_value(self):
        unit = Unit.objects.get(id=1)
        description = unit.description
        self.assertEqual(description, 'gram, one-thousandth of a kilogram in Si')

    def test_object_name_is_unit(self):
        unit = Unit.objects.get(id=1)
        expected_object_name = f'{unit.unit}'
        self.assertEqual(str(unit), expected_object_name)


class QtyModelTest(TestCase):
    """Qty model's test cases."""

    @classmethod
    def setUpTestData(cls):
        Qty.objects.create(amount=100)

    def test_amount_label(self):
        qty = Qty.objects.get(id=1)
        field_label = qty._meta.get_field('amount').verbose_name
        self.assertEqual(field_label, 'amount')

    def test_object_name_is_amount(self):
        qty = Qty.objects.get(id=1)
        expected_object_name = f'{qty.amount}'
        self.assertEqual(str(qty), expected_object_name)


class IngredientModelTest(TestCase):
    """Ingredient model's test cases."""

    @classmethod
    def setUpTestData(cls):
        Ingredient.objects.create(name="sugar")

    def test_name_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_times_used_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('times_used').verbose_name
        self.assertEqual(field_label, 'times used')

    def test_name_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_times_used_value(self):
        ingredient = Ingredient.objects.get(id=1)
        times_used = ingredient.times_used
        self.assertEqual(times_used, 0)

    def test_object_name_is_name(self):
        ingredient = Ingredient.objects.get(id=1)
        expected_object_name = f'{ingredient.name}'
        self.assertEqual(str(ingredient), expected_object_name)


# class RecipeIngredientModelTest(TestCase):
#     """RecipeIngredient model's test cases."""
#
#     @classmethod
#     def setUpTestData(cls):
#         Recipe.objects.create(title='test_pie', description='apple_pie')
#         Unit.objects.create(unit='g', description='gram, one-thousandth of a kilogram in Si')
#         Qty.objects.create(amount=100)
#         Ingredient.objects.create(name="sugar")
#
#         recipe = Recipe.objects.get(id=1)
#         unit = Unit.objects.get(id=1)
#         qty = Qty.objects.get(id=1)
#         ingredient = Ingredient.objects.get(id=1)
#
#         RecipeIngredient.objects.create(
#             recipe=recipe,
#             unit=unit,
#             qty=qty,
#             ingredient=ingredient
#         )
#
#     def test_recipe_labels(self):
#         field_label_recipe = RecipeIngredient.objects.get(id=1)._meta.get_field('recipe').verbose_name
#         field_label_unit = RecipeIngredient.objects.get(id=1)._meta.get_field('unit').verbose_name
#         field_label_qty = RecipeIngredient.objects.get(id=1)._meta.get_field('qty').verbose_name
#         field_label_ingredient = RecipeIngredient.objects.get(id=1)._meta.get_field('ingredient').verbose_name
#         self.assertEqual(field_label_recipe, "recipe")
#         self.assertEqual(field_label_unit, "unit")
#         self.assertEqual(field_label_qty, "qty")
#         self.assertEqual(field_label_ingredient, "ingredient")
