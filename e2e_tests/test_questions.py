from django.urls import reverse

from e2e_tests.testcases import TestCases
from seawatch_registration.models import Question


class TestQuestion(TestCases.SeleniumLoginTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.nav_item = 'Questions'
        self.model_classes = [Question]
        self.nav_item_url = self.live_server_url + reverse('question_list')

        self.login_url = self.live_server_url + reverse('login')
        self.add_url = self.live_server_url + reverse('question_create')

        self.text = 'Hast du Angst vor dem Tod?'

    def test_add_question(self):
        self.login()
        self.click_menu_item_from_index()
        self.click_primary_button()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.add_url)

        self.browser.find_element_by_name('text').send_keys(self.text)
        self.browser.find_element_by_name('mandatory').click()
        self.click_primary_button()

        self.assert_active_navbar()
        self.assertEquals(self.count_table_rows(), 1)
        self.assertTrue(Question.objects.filter(text=self.text, mandatory=True).exists())

    def test_update_question(self):
        question = Question(text=self.text, mandatory=True)
        question.save()
        new_text = 'Führst du ein erfülltes Leben?'
        self.login()
        self.click_menu_item_from_index()
        self.browser.find_element_by_name('edit').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('question_update', kwargs={'pk': question.id}))

        text_input = self.browser.find_element_by_name('text')
        text_input.clear()
        text_input.send_keys(new_text)
        self.browser.find_element_by_name('mandatory').click()
        self.browser.find_element_by_class_name('btn-primary').click()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
        self.assertTrue(Question.objects.filter(text=new_text, mandatory=False).exists())

    def test_delete_question(self):
        question = Question(text=self.text, mandatory=True)
        question.save()
        self.login()
        self.click_menu_item_from_index()
        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('question_delete', kwargs={'pk': question.id}))
        self.click_primary_button()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
        self.assertEquals(len(Question.objects.all()), 0)

    def test_cancel_question_deletion(self):
        question = Question(text=self.text, mandatory=True)
        question.save()
        self.login()
        self.click_menu_item_from_index()
        self.browser.find_element_by_name('delete').click()
        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url,
                          self.live_server_url + reverse('question_delete', kwargs={'pk': question.id}))
        self.browser.find_element_by_link_text('Cancel').click()

        self.assert_active_navbar()
        self.assertEquals(self.browser.current_url, self.nav_item_url)
        self.assertTrue(Question.objects.filter(text=self.text, mandatory=True).exists())
