import factory

from product.models import Product
from product.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("text", max_nb_chars=50)
    slug = factory.Faker("text", max_nb_chars=50)
    description = factory.Faker("text", max_nb_chars=50)
    active = factory.Iterator([True, False])

    class Meta:
        model = Category
        skip_postgeneration_save = True


class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.Faker('pyint')
    category = factory.LazyAttribute(CategoryFactory)
    title = factory.Faker("text", max_nb_chars=50)

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)

    class Meta:
        model = Product
        skip_postgeneration_save = True