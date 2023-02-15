# myapp/management/commands/check_all_translation_fields.py

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Add or remove translation fields for all models based on the LANGUAGES setting'

    def handle(self, *args, **options):
        for model in apps.get_models():
            if hasattr(model, 'check_translation_fields'):
                model.check_translation_fields()
                self.stdout.write(self.style.SUCCESS(f'Translation fields checked for {model.__name__}'))
