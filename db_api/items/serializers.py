from rest_framework import serializers

from core.models import Ingredient, Item, Recipe
from ingredients.serializers import IngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), write_only=True)

    class Meta:
        model = Recipe
        fields = ['ingredient', 'ingredient_id', 'quantity', 'unit']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'type', 'price', 'description']


class ItemSerializer(serializers.ModelSerializer):
    ingredients = RecipeSerializer(source='recipe_set', many=True, required=False)

    class Meta:
        model = Item
        fields = ['id', 'name', 'type', 'price', 'description', 'ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_set', [])
        item = Item.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            ingredient = ingredient_data.pop('ingredient_id')
            Recipe.objects.create(item=item, ingredient=ingredient, **ingredient_data)

        return item

    def update(self, instance, validated_data):
        # TODO item update
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # ingredients_data = validated_data.pop('recipe_set', [])
        # existing_recipes = [recipe.ingredient_id for recipe in instance.recipe_set.all()]


        # print('new: ', ingredients_data)
        # print('existing: ', existing_recipes)
        #
        # for ingredient_data in ingredients_data:
        #     ingredient_id = ingredient_data.pop('ingredient_id')
        #
        #     if ingredient_id in existing_recipes:
        #         recipe = existing_recipes[ingredient_id]
        #         recipe.quantity = ingredient_data.get('quantity', recipe.quantity)
        #         recipe.unit = ingredient_data.get('unit', recipe.unit)
        #         recipe.save()
        #     else:
        #         Recipe.objects.create(
        #             item=instance,
        #             ingredient=ingredient_id,
        #             **ingredient_data
        #         )

        return instance
