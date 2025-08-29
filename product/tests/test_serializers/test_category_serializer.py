import pytest

from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer


@pytest.mark.django_db
def test_category_serializer_create_category():
    data = {
        "title": "Aventura",
        "slug": "aventura",
        "description": "Livros de aventura",
        "active": True
    }

    serializer = CategorySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    category = serializer.save()

    assert isinstance(category, Category)
    assert category.title == "Aventura"
    assert category.active is True