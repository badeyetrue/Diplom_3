from selenium.webdriver.common.by import By


class FeedPageLocators:
    FEED_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    TOTAL_COUNTER = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_COUNTER = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    IN_PROGRESS_ORDERS = (By.XPATH, "//p[text()='В работе:']/following-sibling::ul[1]//li")
