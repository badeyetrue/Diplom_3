import allure
from data.urls import Urls
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException


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
    self.js_click_element(MainPageLocators.INGREDIENT_CARD, scroll=True)

  @allure.step("Проверяем отображение модального окна")
  def is_modal_displayed(self):
    return self.is_element_visible(MainPageLocators.MODAL_WINDOW, time=10)

  @allure.step("Закрываем модальное окно кликом на крестик")
  def close_modal(self):
    self.click_element(MainPageLocators.MODAL_CLOSE_BTN)

  @allure.step("Ожидаем закрытия модального окна")
  def wait_modal_to_disappear(self):
    return self.wait_until_not_visible(MainPageLocators.MODAL_WINDOW)

  @allure.step("Получаем значение счетчика первого ингредиента")
  def get_first_ingredient_counter(self):
    try:
      return int(
          self.find_element(MainPageLocators.INGREDIENT_COUNTER, time=3).text
      )
    except TimeoutException:
      return 0

  @allure.step("Перетаскиваем ингредиент в корзину заказа")
  def add_ingredient_to_order(self):
    self.drag_and_drop_js(
        MainPageLocators.INGREDIENT_CARD, MainPageLocators.BASKET_ZONE
    )

  @allure.step("Оформить заказ")
  def place_order(self):
    self.js_click_element(MainPageLocators.ORDER_BTN)

  @allure.step("Получаем номер созданного заказа из модального окна")
  def get_order_number(self):
    return self.wait_for_digit_text_not_equal(
        MainPageLocators.ORDER_MODAL_NUMBER, "9999", time=20
    )
