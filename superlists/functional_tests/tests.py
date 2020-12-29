import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import LiveServerTestCase
import unittest
import time


MAX_WAIT = 1


class NewVisitorTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome(f"{os.path.abspath('../')}/chromedriver")
        cls.browser.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def check_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time < MAX_WAIT:
                    raise e
                time.sleep(0.5)

    # 사용자 스토리 추가.
    def test_can_start_a_list_and_retriev_it_later(self):
        # 에디스는 투두리스트 웹 어플이 나왔다는 소식을 듣고 확인하러 간다.
        self.browser.get(self.live_server_url)
        # 웹 페이지 타이틀과 헤더가 To-Do를 표시하고 있다.
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)

        # 그녀는 바로 작업을 추가하리고 한다.
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "작업 아이템 입력")

        # 1. 첫 번째 입력
        # "공작깃털 사기"라고 텍스트 상자에 입력한다.
        inputbox.send_keys("공작깃털 사기")
        # 엔터키를 치면 페이지가 갱신되고 작업목록에 "1: 공작깃털 사기" 아이템이 추가된다.
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")
        self.check_for_row_in_list_table("1. 공작깃털 사기")

        # 2. 두 번째 입력
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("공작깃털을 이용해서 그물 만들기")
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn("1. 공작깃털 사기", [row.text for row in rows])
        self.assertIn("2. 공작깃털을 이용해서 그물 만들기", [row.text for row in rows])

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
        # 다시 "공작깃털을 이용해서 그룹 만들기" 라고 입력한다.
        # self.fail("finished test")

        # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보인다.
        self.check_for_row_in_list_table("2. 공작깃털을 이용해서 그물 만들기")
        self.check_for_row_in_list_table("1. 공작깃털 사기")

        # 새로운 사용자인 프란시스가 사이트에 접속한다

        ## 새로운 브라우저 세션을 이용해서 에디스의 정보가 쿠키를 통해 유입되는 것을 방지한다.
        self.browser.quit()
        self.browser = webdriver.Chrome(f"{os.path.abspath('../')}/chromedriver")

        # 프란시스가 홈페이지에 접속한다.
        # 에디스의 리스트는 보이지 않는다.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("공작깃털 사기", page_text)
        self.assertNotIn("그물 만들기", page_text)

        # 프란시스가 새로운 작업 아이템을 입력하기 시작한다.
        # 그는 에디스보다 재미가 없다.
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("우유 사기")
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL을 취득한다.
        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없다는 것을 다시 확인한다.
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("공작깃털 사기", page_text)
        self.assertIn("우유 사기", page_text)


# if __name__ == "__main__":
#     unittest.main(warnings="ignore")

# print(os.getcwd())
# print(os.path.abspath("../../"))
# print(os.path.exists(os.path.abspath("../../chromedriver")))
