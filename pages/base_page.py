import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открыть страницу: {url}")
    def open(self, url):
        self.driver.get(url)

    def find_element(self, locator, time=15):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Не удалось найти элемент по локатору: {locator}"
        )

    def find_elements(self, locator, time=15):
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не удалось найти элементы по локатору: {locator}"
        )

    def click_element(self, locator, time=15):
        element = WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не стал кликабельным"
        )
        element.click()

    def wait_until_not_visible(self, locator, time=15):
        return WebDriverWait(self.driver, time).until(
            EC.invisibility_of_element_located(locator),
            message=f"Элемент {locator} все еще видим"
        )

    def wait_text_to_change(self, locator, old_text, time=15):
        return WebDriverWait(self.driver, time).until(
            lambda d: d.find_element(*locator).text != old_text,
            message="Текст в элементе не изменился"
        )
