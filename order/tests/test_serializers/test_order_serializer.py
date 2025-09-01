import pytest
from django.contrib.auth import get_user_model
from product.models.product import Product
from product.models.category import Category
from order.models import Order
from order.serializers.order_serializer import OrderSerializer


User = get_user_model()

@pytest.mark.django_db
def test_order_serializer_calculates_total():
    user = User.objects.create(username="lucas", password="123456")

    category = Category.objects.create(title="Fantasia", slug="fantasia", description="Livros de fantasia", active=True)

    product1 = Product.objects.create(title="1984", description="Clássico de George Orwell", price=50.0, active=True)
    product1.category.add(category)

    product2 = Product.objects.create(title="O Senhor dos Anéis", description="Trilogia completa", price=120.0, active=True)
    product2.category.add(category)

    order = Order.objects.create(user=user)
    order.product.add(product1, product2)

    serializer = OrderSerializer(order)

    assert serializer.data["total"] == 170.0
    assert len(serializer.data["product"]) == 2