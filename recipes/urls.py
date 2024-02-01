from django.urls import path

from . import views

app_name = "recipes"
urlpatterns = [
    # ex: /recipes/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /recipes/5/
    path("<int:pk>/", views.RecipeIngredientsView.as_view(), name="detail"),
    # ex: /recipes/add_product/1/2/100/ml
    path(
        "add_product/<int:recipe_id>/<int:product_id>/<str:weight>/<str:measure_unit>/",
        views.add_product_to_recipe,
        name="add_product"
    ),
    # ex: /recipes/cook_recipe/1
    path("cook_recipe/<int:recipe_id>/", views.cook_recipe, name="cook_recipe"),
    # ex: /recipes/without_product/1
    path("without_product/<int:product_id>/", views.show_recipes_without_product, name="without_product")
]
