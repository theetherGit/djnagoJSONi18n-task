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

#### Pros of using JSONField to store translations

- Simplified database schema: Using a single JSONField to store translations simplifies the database schema as there is no need to create a separate table to store translations.
- Flexible and extensible: JSON is a flexible data format that can store complex data structures. This makes it easy to extend the translation system to include additional metadata or properties as needed.
- Easy to use: Working with JSON data in Python is straightforward as it can be loaded into a Python dictionary, allowing for easy access to translations in different languages.

#### Cons of using JSONField to store translations

- Limited querying capability: As the translations are stored in a single field, querying the database to find all instances of a certain translated term can be difficult. This can be addressed by using a specialized indexing solution, but this requires additional setup and configuration.
- Potential performance issues: As the size of the JSONField grows, querying and updating records can become slower. Additionally, searching within the JSON data can be slower than querying a dedicated translation table. However, these issues may not be noticeable until a large number of records are present.

### Task Two: Tree - (optional) - Haven't tried yet.

Let’s look at the following simple tree: 
where `A` is `parent` to `B` and `C`, `B` is `parent` to `D` and `E`.

How would you implement such a data model in any `RDBMS`? Please provide your
thoughts or even add a simple code snippet (Django-based would be great). What are possible
approaches and pros/cons? How does `D` node relate to `A` node? Imagine there are `10 000`
items and `depth level` is `10`. How would you count number of `descendants` (e.g., for A count
B + D + E) of any node on the first level?

#### Answers

-To implement such a data model in an RDBMS, My approach is to use a column for the parent-child relationship. 
This column would contain the ID of the parent for each child. For example, for Node A, the column would contain null, 
for Node B and C it would contain the ID of Node A, for Node D and E it would contain the ID of Node B, and so on.
- Here, I'm using a django specific package `django-mptt` for this which provide extra functionality out of the box.
- Implementation
  ```python
  # tree/models.py
  
  from django.db import models
  from mptt.models import MPTTModel, TreeForeignKey
  
  
  class TreeNode(MPTTModel):
      name = models.CharField(max_length=255)
      parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
  
      class MPTTMeta:
          order_insertion_by = ['name']
  
      def __str__(self):
          return f"{self.name} - {self.get_descendant_count()}"
  ```
  
#### Pros of using MPTT
- Easy to understand and implement.
- Easier to query data that is organized into a tree structure. This can be especially useful when dealing with large datasets. (Fast readability)
- Easily scaled to accommodate large data sets by adding additional columns and rows as needed

#### Cons of using MPTT
- Slow writes
- Hard to make changes to the parent-child relationships when they are stored in a single column.

#### How does `D` node relate to `A` node?
Node D relates to Node A through its parent-child relationship. Node D is a descendant of Node A, as it is a child of Node B, which is a child of Node A.

#### Counting Descendants
- To count the number of descendants of any node on the first level, you would need 
to perform a recursive query that counts the number of children of each node, 
starting from the first level. This query would need to be run on each node in the 
tree, and the results would need to be aggregated to get the total number of 
descendants. This could become very slow if the tree has a large number of items and 
a large depth level.
- 
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
