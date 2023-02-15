from django.test import TestCase

from .widget import JsonInputWidget


class TestFlatJsonWidget(TestCase):
    def test_render(self):
        widget = JsonInputWidget()
        html = widget.render(name='content', value=None)
        self.assertIn('flat-json-original-textarea', html)
        self.assertIn('flat-json-textarea', html)
        self.assertIn('icon-changelink.svg', html)

    def test_media(self):
        widget = JsonInputWidget()
        html = widget.media.render()
        expected_list = [
            '/static/jsonWidget/css/json-widget.css',
            '/static/jsonWidget/js/lib/underscore.js',
            '/static/jsonWidget/js/json-widget.js',
        ]
        for expected in expected_list:
            self.assertIn(expected, html)