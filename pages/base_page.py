import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:

  def __init__(self, driver):
    self.driver = driver

  @allure.step("Открыть страницу: {url}")
  def open(self, url):
    self.driver.get(url)

  def find_element(self, locator, time=15):
    return WebDriverWait(self.driver, time).until(
        EC.presence_of_element_located(locator),
        message=f"Не удалось найти элемент по локатору: {locator}",
    )

  def find_elements(self, locator, time=15):
    return WebDriverWait(self.driver, time).until(
        EC.presence_of_all_elements_located(locator),
        message=f"Не удалось найти элементы по локатору: {locator}",
    )

  def find_visible_element(self, locator, time=15):
    return WebDriverWait(self.driver, time).until(
        EC.visibility_of_element_located(locator),
        message=f"Элемент {locator} не стал видимым",
    )

  def is_element_visible(self, locator, time=10):
    try:
      self.find_visible_element(locator, time=time)
      return True
    except TimeoutException:
      return False

  def click_element(self, locator, time=15):
    element = WebDriverWait(self.driver, time).until(
        EC.element_to_be_clickable(locator),
        message=f"Элемент {locator} не стал кликабельным",
    )
    element.click()

  def js_click_element(self, locator, time=15, scroll=False):
    element = (
        self.find_visible_element(locator, time=time)
        if scroll
        else WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не стал кликабельным",
        )
    )
    if scroll:
      self.driver.execute_script(
          "arguments[0].scrollIntoView({block: 'center'});", element
      )
    self.driver.execute_script("arguments[0].click();", element)

  def drag_and_drop_js(self, source_locator, target_locator, time=15):
    source = self.find_visible_element(source_locator, time=time)
    target = self.find_visible_element(target_locator, time=time)

    js_script = """
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
    self.driver.execute_script(js_script, source, target)

  def wait_until_not_visible(self, locator, time=15):
    return WebDriverWait(self.driver, time).until(
        EC.invisibility_of_element_located(locator),
        message=f"Элемент {locator} все еще видим",
    )

  def wait_text_to_change(self, locator, old_text, time=15):
    return WebDriverWait(self.driver, time).until(
        lambda d: d.find_element(*locator).text != old_text,
        message="Текст в элементе не изменился",
    )

  def wait_for_text_in_elements(self, locator, texts, time=15):
    try:
      WebDriverWait(self.driver, time).until(
          lambda d: any(
              any(text in item.text for text in texts)
              for item in d.find_elements(*locator)
          )
      )
      return True
    except TimeoutException:
      return False

  def wait_for_digit_text_not_equal(self, locator, excluded_text, time=20):
    self.find_visible_element(locator, time=time)
    WebDriverWait(self.driver, time).until(
        lambda d: d.find_element(*locator).text != excluded_text
        and d.find_element(*locator).text.strip().isdigit()
    )
    return self.find_element(locator).text.strip()
