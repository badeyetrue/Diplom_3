from selenium.webdriver.common.by import By

class MainPageLocators:
    CONSTRUCTOR_BTN = (By.XPATH, "//p[contains(text(), 'Конструктор')]/parent::a")
    FEED_BTN = (By.XPATH, "//p[contains(text(), 'Лента Заказов')]/parent::a")
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")
    
    # Ингредиенты
    INGREDIENT_CARD = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__')]")
    INGREDIENT_COUNTER = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient__')]//p[contains(@class, 'counter_counter__num__')]")
    
    # Зона корзины
    BASKET_ZONE = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket__')]")
    
    # Модальное окно деталей ингредиента
    MODAL_WINDOW = (By.XPATH, "//*[text()='Детали ингредиента']/ancestor::div[contains(@class, 'Modal_modal__')]")
    MODAL_CLOSE_BTN = (By.XPATH, "//*[text()='Детали ингредиента']/parent::div/following-sibling::button | //button[contains(@class, 'Modal_modal_closed__')]")
    
    # Оформление заказа
    ORDER_BTN = (By.XPATH, "//button[contains(@class, 'button_button_type_primary__')]")
    ORDER_MODAL_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title_shadow__')]")

# �������� UI
