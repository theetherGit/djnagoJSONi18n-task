## Wodasoft Corporation Backend Task

In this project, I had to solve two tasks where second task is optional. First task is to add Django i18n support with JsonField and Second Task is about tree and node dependencies, It's the optional one.


### Task One: Django i18n Support with JSONField

In general, this task supposes to just implement a JsonField based i18n support to Django which 
means I have to save data of that field on the bases of language code and then in admin panel 
I have to show JsonField data as text field for every key as language. If we add or remove support for
any language then we should be able to update data and fields on the basis of language added or deleted.

#### Approach

- Extend JsonField with custom name such as `JsonTranslationField` and then add another class such as `JsonTranslationMethods` which will extend our 
model methods for getting translated values on the bases of language code and will as `@classmethod` that will help to 
update database entries when we add or remove language support with simple command like:
    ```bash
    python manage.py check_translation_fields
    ```
- Add a widget such as `JsonInputWidget` for json view in admin panel which we can use on our model form and add it to our JSONField. For now, it only supports Input Field, but we can also add another widget for textarea.

#### Examples

- Using `JsonTranslationField` and `JsonTranslationMethods` in a Django model

    ```python
    # i18nJson/models.py

    from django.db import models
    from jsonTranslationExtension.JsonTranslation import JsonTranslationField, JsonTranslationMethods
    from core.settings import LANGUAGES, LANGUAGE_CODE
    from django.utils.translation import gettext_lazy as _

    language_dict = {key: '' for key, _ in LANGUAGES}

        
    class Article(models.Model, JsonTranslationMethods):
        title = JsonTranslationField(_('Title'), default=language_dict)

        class Meta:
            verbose_name_plural = _('articles')

        def __str__(self):
            return f"Article Title with get_translated_fields : {self.get_translated_fields('title')}, Title with LANGUAGE_CODE: {self.title[LANGUAGE_CODE]}"
    ```
  > As you can see, we have added `JsonTranslationMethods` to our model class and used `JsonTranslationField` using default values 
  > as language key based dict. Now we need to add form and our widget to show key form on title field for Input Field like view. Make sure to run makemigrations and migrate.

- Adding form with `JsonInputWidget` to tile field.
    ```python
    # i18nJson/forms.py
    
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
    ```
  > Here we used `JsonInputWidget` in our article form's `title` field. Now we just need to add all these things to the admin.py,
  > so we use it in admin panel.
  
- Adding form and model to `admin.py` to use admin panel for test of our widget.
    ```python
    # i18nJson/admin.py
    
    from django.contrib import admin
    from i18nJson.forms import ArticleForm
    from i18nJson.models import Article
    
    
    @admin.register(Article)
    class ArticleAdmin(admin.ModelAdmin):
        form = ArticleForm
    ```
  > Now we have added the form and model, we are going to access our django admin panel for that we need to createsuperuser.
  > Do that and access admin panel and use your jsonField as a translation field.
  
### Task Two: Tree - (optional) - Haven't tried yet.

## Test on your system

- Clone this repository
    ```bash
    git clone https://github.com/theetherGit/djnagoJSONi18n-task.git
    ```
- Change directory to `djnagoJSONi18n-task`.
- Install all the required dependencies
    ```bash
    pip install -r requirements.txt 
    ```
- Migrate all migration and then create superuser.
    ```bash
    python manage.py migrate
    ```
    ```bash
    python manage.py createsuperuser
    ```
  > For createsuperuser you have to provide name, email and password.

- Run dev server
    ```bash
    python manage.py runserver 
    ```
  > This will run a dev server on ` http://127.0.0.1:8000/` now you can go to 
  > `http://127.0.0.1:8000/admin/` then you need login to admin panel
  > then you can play with it.
