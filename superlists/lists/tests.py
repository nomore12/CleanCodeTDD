import re

from django.test import TestCase, SimpleTestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item


def remove_csrf_tag(text):
    return re.sub(r"<[^>]*csrfmiddlewaretoken[^>]*>", "", text)


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
        # HTML은 assertHTMLEqual으로 테스트 가능.
        self.assertHTMLEqual(
            remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html)
        )
        self.assertEqual(remove_csrf_tag(response.content.decode()), remove_csrf_tag(expected_html))

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = "신규 작업 아이템"
        response = home_page(request)
        self.assertIn("신규 작업 아이템", response.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "첫 번째 아이템"
        first_item.save()

        second_item = Item()
        second_item.text = "두 번째 아이템"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, "첫 번째 아이템")
        self.assertEqual(second_saved_item.text, "두 번째 아이템")
