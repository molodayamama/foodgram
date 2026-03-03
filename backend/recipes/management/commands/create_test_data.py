import random

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Recipe, RecipeIngredient
from users.models import User

RECIPES = [
    ('Борщ', 'Классический украинский борщ со свёклой и сметаной.', 90),
    ('Оливье', 'Традиционный новогодний салат с колбасой и горошком.', 30),
    ('Пельмени', 'Домашние пельмени с говядиной и свининой.', 120),
    ('Блины', 'Тонкие блины на молоке к масленице.', 40),
    ('Солянка', 'Острый суп с копчёностями и оливками.', 75),
    ('Котлеты', 'Сочные котлеты по-домашнему из смешанного фарша.', 45),
    ('Пицца', 'Домашняя пицца с томатным соусом и моцареллой.', 60),
    ('Тирамису', 'Итальянский десерт с кофе и маскарпоне.', 20),
    ('Гречка с грибами', 'Рассыпчатая гречневая каша с жареными грибами.', 35),
    ('Сырники', 'Пышные сырники из творога на завтрак.', 25),
]

USERS = [
    ('chef2@food.com', 'chef2', 'Анна', 'Кулинарова', 'Chef2024!'),
    ('cook3@food.com', 'cook3', 'Сергей', 'Вкусный', 'Cook2024!'),
]


class Command(BaseCommand):
    help = 'Create test users and recipes'

    def handle(self, *args, **options):
        ingredients = list(Ingredient.objects.all()[:50])
        if not ingredients:
            self.stderr.write('No ingredients found. Run load_ingredients first.')
            return

        users = []
        for email, username, first, last, pwd in USERS:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first,
                    'last_name': last,
                },
            )
            if created:
                user.set_password(pwd)
                user.save()
                self.stdout.write(f'Created user: {username} / {pwd}')
            users.append(user)

        # Also include existing users
        users += list(User.objects.exclude(email__in=[u[0] for u in USERS])[:3])

        created_count = 0
        for i, (name, text, time) in enumerate(RECIPES):
            author = users[i % len(users)]
            if Recipe.objects.filter(name=name).exists():
                continue
            recipe = Recipe.objects.create(
                author=author,
                name=name,
                text=text,
                cooking_time=time,
                image='recipes/images/default.jpg',
            )
            sample = random.sample(ingredients, min(4, len(ingredients)))
            RecipeIngredient.objects.bulk_create([
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=ing,
                    amount=random.randint(10, 500),
                )
                for ing in sample
            ])
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Created {created_count} recipes for {len(users)} users.'
            )
        )
