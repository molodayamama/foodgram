import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            default='/app/data/ingredients.json',
            help='Path to the ingredients JSON file',
        )

    def handle(self, *args, **options):
        path = options['path']
        if not os.path.exists(path):
            self.stderr.write(f'File not found: {path}')
            return
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        ingredients = [
            Ingredient(name=item['name'], measurement_unit=item['measurement_unit'])
            for item in data
        ]
        created = Ingredient.objects.bulk_create(
            ingredients, ignore_conflicts=True
        )
        self.stdout.write(
            self.style.SUCCESS(f'Loaded {len(created)} ingredients.')
        )
