from django.contrib import admin

from .models import Recipe, Unit, Qty, Ingredient, RecipeIngredient


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    fields = ["ingredient", "qty", "unit"]
    extra = 3


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        ("RECIPE", {"fields": ["title", "description"]}),
        ("DATE INFORMATION", {"fields": ["pub_date"]}),
    ]
    list_display = ["title", "pub_date", "was_published_recently"]
    list_filter = ['pub_date']
    search_fields = ["title"]
    inlines = [RecipeIngredientsInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Unit)
admin.site.register(Qty)
admin.site.register(Ingredient)
