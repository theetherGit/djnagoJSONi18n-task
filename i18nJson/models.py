from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonTranslationExtension.JsonTranslation import JsonTranslationField, JsonTranslationMethods
from core.settings import LANGUAGES, LANGUAGE_CODE

language_dict = {key: '' for key, _ in LANGUAGES}


class Article(models.Model, JsonTranslationMethods):
    """
    In model class we have extended it with JsonTranslationMethods and then  added JsonTranslationField.
    """
    title = JsonTranslationField(_('Title'), default=language_dict)

    class Meta:
        verbose_name_plural = _('articles')

    def __str__(self):
        return f"Article Title with get_translated_fields : {self.get_translated_fields('title')}, Title with LANGUAGE_CODE: {self.title[LANGUAGE_CODE]}"
