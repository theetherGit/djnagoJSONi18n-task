from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget
from django.template.loader import get_template
from django.utils.safestring import mark_safe


class JsonInputWidget(AdminTextareaWidget):
    """
    JSON Key/Value widget to show value as input field
    """

    @property
    def media(self):
        internal_js = ['lib/underscore.js', 'json-widget.js']
        js = ['admin/js/jquery.init.js'] + [
            f'jsonWidget/js/{path}' for path in internal_js
        ]
        css = {'all': ('jsonWidget/css/json-widget.css',)}
        return forms.Media(js=js, css=css)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        # it's called "original" because it will be replaced by a copy
        attrs['class'] = 'flat-json-original-textarea'
        html = super().render(name, value, attrs)
        template = get_template('jsonWidget/json-widget.html')
        html += template.render({'field_name': name})
        return mark_safe(html)
