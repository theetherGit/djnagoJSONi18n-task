# Generated by Django 4.1.7 on 2023-02-15 09:49

from django.db import migrations, models
import jsonTranslationExtension.JsonTranslation


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', jsonTranslationExtension.JsonTranslation.JsonTranslationField(default={'en': '', 'fr': ''}, verbose_name='Title')),
            ],
            options={
                'verbose_name_plural': 'articles',
            },
            bases=(models.Model, jsonTranslationExtension.JsonTranslation.JsonTranslationMethods),
        ),
    ]
