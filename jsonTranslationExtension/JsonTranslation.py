from django.db import models

from core import settings

language_dict = {key: '' for key, _ in settings.LANGUAGES}


class JsonTranslationField(models.JSONField):
    """
    JsonTranslationField is just an extension field for JSONField. The sole reason to have this is to identify
    translation fields in models, so we can update model data when we change language settings e.g. remove or add a
    language codes in Settings Language Object.

    When you are using JsonTranslationField for translations make sure to use default values as follows:
    language_dict = {key: '' for key, _ in settings.LANGUAGES}
    field_name = JsonTranslationField(_('field_name'), default=language_dict)
    """
    pass


class JsonTranslationMethods:
    """
    JsonTranslationMethods is a model extension for your model where JsonTranslationField is being used.
    This provides us two methods get_translated_fields(field_name, language) and check_translation_fields()

    1. get_translated_fields helps to get default translation value on the bases of LANGUAGE_CODE that we define in
    Django settings. This take two parameters field_name and language(optional) if you want to get language value different
    from Default Language you have to provide it with code of that language. If by mistake you provide wrong language
    code then it will return None and print the message 'Invalid language code: {language}'.

    2. check_translation_fields: This method is used with command by the same name. The only way I can update language
    field if we add/remove language from settings.
    Command: python manage.py check_translation_fields
    run this and in every model you have used JsonTranslationMethods to extend model this will check for
    JsonTranslationField in your model field if field found then going to check for default value is languages dict.
    If everything satisfies it's going to add/remove language code to your JsonTranslationField.
    For Example Check i18nJson app models, form and admin python files.
    """

    def get_translated_fields(self, field_name, language=settings.LANGUAGE_CODE):
        if language in language_dict:
            field_value = getattr(self, field_name)
            return field_value.get(language)
        else:
            print(f'Invalid language code: {language}')
            return None

    @classmethod
    def check_translation_fields(cls):
        current_languages = {lang[0] for lang in settings.LANGUAGES}
        model_trans_fields = [
            field.name for field in cls._meta.fields
            if isinstance(field, JsonTranslationField) and field.default == language_dict
        ]
        if model_trans_fields:
            for data in cls.objects.all():
                for field in model_trans_fields:
                    print(f'starting {data.id} - {field} fields update')
                    current_field_data = getattr(data, field)
                    field_changes = {}
                    existing_languages = set(current_field_data.keys())
                    required_languages = set(current_languages.difference(existing_languages))
                    un_required_languages = existing_languages.difference(current_languages)
                    if required_languages:
                        field_changes['added_languages'] = list(required_languages)
                        for language in required_languages:
                            current_field_data[language] = ''
                    if un_required_languages:
                        field_changes['removed_languages'] = list(un_required_languages)
                        for language in un_required_languages:
                            current_field_data.pop(language)
                    if field_changes:
                        setattr(data, field, current_field_data)
                        data.save()
                    print(f'ending {data.id} - {field} fields update')
        else:
            print(f"Provide JsonTranslationField is not valid for this method in {cls.__name__}")
