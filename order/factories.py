import factory

from django.contrib.auth.models import User
from product.factories import ProductFactory

from order.models import Order

class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("text", max_nb_chars=20)
    username = factory.Faker("text", max_nb_chars=20)

    class Meta:
        model = User
        skip_postgeneration_save = True


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.product.add(product)

    class Meta:
        model = Order
        skip_postgeneration_save = True