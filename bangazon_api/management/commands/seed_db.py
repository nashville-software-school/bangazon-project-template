import random
import faker_commerce
from faker import Faker
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from bangazon_api.models import Store, Product, Category, PaymentType


class Command(BaseCommand):
    faker = Faker()
    faker.add_provider(faker_commerce.Provider)

    state_names = [
        "Alaska", "Alabama", "Arkansas", "Arizona", "California",
        "Colorado", "Connecticut", "District ", "of Columbia",
        "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho",
        "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana",
        "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota",
        "Missouri", "Mississippi", "Montana", "North Carolina",
        "North Dakota", "Nebraska", "New Hampshire", "New Jersey",
        "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon",
        "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
        "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington",
        "Wisconsin", "West Virginia", "Wyoming"
    ]

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            '--user_count',
            help='Count of users to seed',
        )
    def handle(self, *args, **options):
        if options['user_count']:
            self.create_users(int(options['user_count']))
        else:
            self.create_users()

    def create_users(self, user_count=10):
        for _ in range(user_count):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = f'{first_name}_{last_name}@example.com'
            user = User.objects.create_user(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                password="PassWord1",
                username=username,
            )
            print(f'Added user: {user.get_full_name()}')

            PaymentType.objects.create(
                customer=user,
                merchant_name=self.faker.credit_card_provider(),
                acct_number=self.faker.credit_card_number()
            )

            Token.objects.create(
                user=user
            )

            if user.id % 2 == 0:
                store = self.create_store(user)
                print(f'Added store: {store.name}')
                self.create_products(store, user_count)

    def create_store(self, user):
        return Store.objects.create(
            seller=user,
            name=self.faker.company(),
            description=self.faker.paragraph(),
            is_active=True
        )

    def create_products(self, store, count):
        for _ in range(count):
            product = Product.objects.create(
                name=self.faker.ecommerce_name(),
                store=store,
                price=random.randint(50, 1000),
                description=self.faker.paragraph,
                quantity=random.randint(2, 20),
                location=random.choice(self.state_names),
                image_path="",
                category=Category.objects.get_or_create(
                    name=self.faker.ecommerce_category())[0]
            )
            print(f'Added product: {product.name}')
