import pytest
from product.models.product import Product, Category
from product.serializers.product_serializer import ProductSerializer

@pytest.mark.django_db
def test_product_serializer_returns_category_data():
    category = Category.objects.create(
        title="Romance",
        slug="romance",
        description="Livros de romance",
        active=True
    )

    product = Product.objects.create(
        title="Orgulho e Preconceito",
        description="Clássico da literatura",
        price=39,
        active=True,
    )
    product.category.add(category)

    serializer = ProductSerializer(product)

    data = serializer.data

    assert data["title"] == "Orgulho e Preconceito"
    assert data["price"] == 39
    assert data["category"][0]["title"] == "Romance"
    assert data["category"][0]["slug"] == "romance"
