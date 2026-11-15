import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from data.urls import Urls
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):

    @allure.step("Открыть главную страницу «Конструктор»")
    def open_main_page(self):
        self.open(Urls.BASE_URL)

    @allure.step("Кликаем на кнопку 'Конструктор'")
    def click_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BTN)

    @allure.step("Кликаем на кнопку 'Лента Заказов'")
    def click_feed(self):
        self.click_element(MainPageLocators.FEED_BTN)

    @allure.step("Проверяем отображение заголовка Конструктора")
    def is_constructor_title_displayed(self):
        return self.find_element(MainPageLocators.CONSTRUCTOR_TITLE).is_displayed()

    @allure.step("Кликаем по первому ингредиенту")
    def click_first_ingredient(self):
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(MainPageLocators.INGREDIENT_CARD)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Проверяем отображение модального окна")
    def is_modal_displayed(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.MODAL_WINDOW)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Закрываем модальное окно кликом на крестик")
    def close_modal(self):
        self.click_element(MainPageLocators.MODAL_CLOSE_BTN)

    @allure.step("Ожидаем закрытия модального окна")
    def wait_modal_to_disappear(self):
        return self.wait_until_not_visible(MainPageLocators.MODAL_WINDOW)

    @allure.step("Получаем значение счетчика первого ингредиента")
    def get_first_ingredient_counter(self):
        try:
            return int(self.find_element(MainPageLocators.INGREDIENT_COUNTER, time=3).text)
        except TimeoutException:
            return 0

    @allure.step("Перетаскиваем ингредиент в корзину заказа")
    def add_ingredient_to_order(self):
        source = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(MainPageLocators.INGREDIENT_CARD)
        )
        target = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(MainPageLocators.BASKET_ZONE)
        )

        js_drag_and_drop = """
        function createEvent(typeOfEvent) {
            var event = document.createEvent("CustomEvent");
            event.initCustomEvent(typeOfEvent, true, true, null);
            event.dataTransfer = {
                data: {},
                setData: function (key, value) { this.data[key] = value; },
                getData: function (key) { return this.data[key]; }
            };
            return event;
        }
        function dispatchEvent(element, event, transferData) {
            if (transferData !== undefined) { event.dataTransfer = transferData; }
            if (element.dispatchEvent) { element.dispatchEvent(event); }
            else if (element.fireEvent) { element.fireEvent("on" + event.type, event); }
        }
        function dragAndDrop(element, target) {
            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(element, dragStartEvent);
            var dropEvent = createEvent('drop', dragStartEvent.dataTransfer);
            dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);
            var dragEndEvent = createEvent('dragend', dragStartEvent.dataTransfer);
            dispatchEvent(element, dragEndEvent);
        }
        dragAndDrop(arguments[0], arguments[1]);
        """
        self.driver.execute_script(js_drag_and_drop, source, target)

    @allure.step("Оформить заказ")
    def place_order(self):
        btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(MainPageLocators.ORDER_BTN)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    @allure.step("Получаем номер созданного заказа из модального окна")
    def get_order_number(self):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(MainPageLocators.ORDER_MODAL_NUMBER)
        )

        WebDriverWait(self.driver, 20).until(
            lambda d: d.find_element(*MainPageLocators.ORDER_MODAL_NUMBER).text != "9999" and
                      d.find_element(*MainPageLocators.ORDER_MODAL_NUMBER).text.strip().isdigit()
        )

        return self.find_element(MainPageLocators.ORDER_MODAL_NUMBER).text.strip()
