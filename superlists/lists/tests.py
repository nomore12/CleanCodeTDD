from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string


# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolve_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        # 상수를 테스트하는 것이 아니라 구현 결과물을 비교하는 것.
        # 이전 코드에는 하드코딩된 html으로 test했지만, 이번엔 templates의 home.html로 비교.
        expected_html = render_to_string("home.html")
        self.assertEqual(response.condent.decode(), expected_html)
