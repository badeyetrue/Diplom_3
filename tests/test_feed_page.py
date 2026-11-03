import allure
import time
from data.urls import Urls
from pages.main_page import MainPage
from pages.feed_page import FeedPage

@allure.suite("Раздел «Лента заказов»")
class TestFeedPage:

    @allure.title("При создании нового заказа счётчик «Выполнено за всё время» увеличивается")
    def test_total_orders_counter_increases(self, driver, create_user_and_auth):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        
        driver.get(Urls.FEED_URL)
        initial_total = feed_page.get_total_orders_count()
        
        driver.get(Urls.BASE_URL)
        main_page.add_ingredient_to_order()
        time.sleep(1)  # Даем UI секунду на пересчет корзины
        main_page.place_order()
        main_page.get_order_number()
        
        driver.get(Urls.FEED_URL)
        feed_page.wait_total_orders_count_to_change(initial_total)
        new_total = feed_page.get_total_orders_count()
        assert new_total == initial_total + 1

    @allure.title("При создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_today_orders_counter_increases(self, driver, create_user_and_auth):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        
        driver.get(Urls.FEED_URL)
        initial_today = feed_page.get_today_orders_count()
        
        driver.get(Urls.BASE_URL)
        main_page.add_ingredient_to_order()
        time.sleep(1)
        main_page.place_order()
        main_page.get_order_number()
        
        driver.get(Urls.FEED_URL)
        feed_page.wait_today_orders_count_to_change(initial_today)
        new_today = feed_page.get_today_orders_count()
        assert new_today == initial_today + 1

    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    def test_order_number_appears_in_progress(self, driver, create_user_and_auth):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        
        driver.get(Urls.BASE_URL)
        main_page.add_ingredient_to_order()
        time.sleep(1)
        main_page.place_order()
        order_number = main_page.get_order_number()
        
        driver.get(Urls.FEED_URL)
        assert feed_page.is_order_in_progress(order_number)
