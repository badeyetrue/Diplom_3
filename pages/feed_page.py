import allure
from data.urls import Urls
from locators.feed_page_locators import FeedPageLocators
from pages.base_page import BasePage


class FeedPage(BasePage):

  @allure.step("Открыть страницу «Лента заказов»")
  def open_feed_page(self):
    self.open(Urls.FEED_URL)

  @allure.step("Проверяем отображение заголовка Ленты заказов")
  def is_feed_title_displayed(self):
    return self.find_element(FeedPageLocators.FEED_TITLE).is_displayed()

  @allure.step("Получаем счетчик 'Выполнено за все время'")
  def get_total_orders_count(self):
    return int(self.find_element(FeedPageLocators.TOTAL_COUNTER).text)

  @allure.step("Ожидаем изменения счетчика 'Выполнено за все время'")
  def wait_total_orders_count_to_change(self, old_value):
    return self.wait_text_to_change(
        FeedPageLocators.TOTAL_COUNTER, str(old_value)
    )

  @allure.step("Получаем счетчик 'Выполнено за сегодня'")
  def get_today_orders_count(self):
    return int(self.find_element(FeedPageLocators.TODAY_COUNTER).text)

  @allure.step("Ожидаем изменения счетчика 'Выполнено за сегодня'")
  def wait_today_orders_count_to_change(self, old_value):
    return self.wait_text_to_change(
        FeedPageLocators.TODAY_COUNTER, str(old_value)
    )

  @allure.step(
      "Проверяем наличие номера заказа {order_number} в разделе «В работе»"
  )
  def is_order_in_progress(self, order_number):
    clean_number = order_number.replace("#", "").strip()
    formatted_number = clean_number.zfill(6)

    return self.wait_for_text_in_elements(
        FeedPageLocators.IN_PROGRESS_ORDERS,
        [formatted_number, clean_number],
        time=20,
    )
