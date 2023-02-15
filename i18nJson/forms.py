from django import forms
from core.settings import LANGUAGE_CODE
from jsonTranslationExtension.widget import JsonInputWidget


class ArticleForm(forms.ModelForm):
    class Meta:
        widgets = {
            'title': JsonInputWidget
        }

    def clean(self):
        if self.cleaned_data.get('title').get(LANGUAGE_CODE) == '':
            raise forms.ValidationError(f"Must provide default language title {LANGUAGE_CODE}")
        return self.cleaned_data
