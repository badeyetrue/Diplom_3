import allure
from pages.main_page import MainPage
from pages.feed_page import FeedPage


@allure.suite("Проверка основной функциональности")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    def test_navigate_to_constructor(self, driver):
        feed_page = FeedPage(driver)
        main_page = MainPage(driver)
        feed_page.open_feed_page()
        main_page.click_constructor()
        assert main_page.is_constructor_title_displayed()

    @allure.title("Переход по клику на раздел «Лента заказов»")
    def test_navigate_to_feed(self, driver):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        main_page.open_main_page()
        main_page.click_feed()
        assert feed_page.is_feed_title_displayed()

    @allure.title("Появление всплывающего окна при клике на ингредиент")
    def test_ingredient_modal_open(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_first_ingredient()
        assert main_page.is_modal_displayed()

    @allure.title("Закрытие всплывающего окна кликом по крестику")
    def test_ingredient_modal_close(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        main_page.click_first_ingredient()
        main_page.close_modal()
        assert main_page.wait_modal_to_disappear()

    @allure.title("Увеличение счетчика ингредиента при добавлении в заказ")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()
        initial_counter = main_page.get_first_ingredient_counter()
        main_page.add_ingredient_to_order()
        new_counter = main_page.get_first_ingredient_counter()
        assert new_counter > initial_counter
