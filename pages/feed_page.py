import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from locators.feed_page_locators import FeedPageLocators

class FeedPage(BasePage):

    @allure.step("Проверяем отображение заголовка Ленты заказов")
    def is_feed_title_displayed(self):
        return self.find_element(FeedPageLocators.FEED_TITLE).is_displayed()

    @allure.step("Получаем счетчик 'Выполнено за все время'")
    def get_total_orders_count(self):
        return int(self.find_element(FeedPageLocators.TOTAL_COUNTER).text)

    @allure.step("Ожидаем изменения счетчика 'Выполнено за все время'")
    def wait_total_orders_count_to_change(self, old_value):
        return self.wait_text_to_change(FeedPageLocators.TOTAL_COUNTER, str(old_value))

    @allure.step("Получаем счетчик 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        return int(self.find_element(FeedPageLocators.TODAY_COUNTER).text)

    @allure.step("Ожидаем изменения счетчика 'Выполнено за сегодня'")
    def wait_today_orders_count_to_change(self, old_value):
        return self.wait_text_to_change(FeedPageLocators.TODAY_COUNTER, str(old_value))

    @allure.step("Проверяем наличие номера заказа на странице")
    def is_order_in_progress(self, order_number):
        # Получаем чистый номер ("1033") и шестизначный формат ("001033")
        clean_number = order_number.replace("#", "").strip()
        formatted_number = clean_number.zfill(6)
        
        # Даем WebSocket-ленте 3 секунды обновиться после перехода
        time.sleep(3)
        
        try:
            # Ищем номер просто по всему тексту страницы (внутри тега body)
            WebDriverWait(self.driver, 20).until(
                lambda d: formatted_number in d.find_element(By.TAG_NAME, "body").text or 
                         clean_number in d.find_element(By.TAG_NAME, "body").text,
                message=f"Номер заказа {clean_number} не найден на странице Ленты"
            )
            return True
        except Exception:
            return False
