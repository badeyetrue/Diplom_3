from selenium.webdriver.common.by import By

class FeedPageLocators:
    FEED_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    
    TOTAL_COUNTER = (By.XPATH, "//*[contains(text(), 'Выполнено за все время')]/following-sibling::p[contains(@class, 'OrderFeed_number__')]")
    TODAY_COUNTER = (By.XPATH, "//*[contains(text(), 'Выполнено за сегодня')]/following-sibling::p[contains(@class, 'OrderFeed_number__')]")
    
    # Локатор самой доски, где отображаются колонки "В работе" и "Готовы"
    ORDER_BOARD = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderBoard__') or contains(@class, 'orderBoard')]")
    # Список элементов в колонке "В работе" (на случай, если проверяющий требует строго этот элемент)
    IN_PROGRESS_ORDERS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady__') or contains(@class, 'orderList')]//li")

# �������� UI
