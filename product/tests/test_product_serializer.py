import pytest
from unicodedata import category

from product.models.product import Product
from product.models.category import Category
from product.serializers.product_serializer import ProductSerializer


@pytest.mark.django_db
def test_product_serializer_creates_product():
    data = {
        "title": "Orgulho e Preconceito",
        "description": "Clássico da literatura",
        "price": 39,
        "active": True,
        "category": [
            {
                "title": "Romance",
                "slug": "romance",
                "description": "Livros de romance",
                "active": True
            }
        ]
    }

    serializer = ProductSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    product = serializer.save()

    assert isinstance(product, Product)
    assert product.title == "Orgulho e Preconceito"
    assert product.price == 39
    assert product.category.first().title == "Romance"