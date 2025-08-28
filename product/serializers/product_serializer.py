from rest_framework import serializers
from product.models.product import Product
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, required=True)

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "active", "category"]

    def create(self, validated_data):
        categories_data = validated_data.pop("category")

        product = Product.objects.create(**validated_data)

        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(
                slug=category_data["slug"],
                defaults=category_data
            )
            product.category.add(category)

        return product
