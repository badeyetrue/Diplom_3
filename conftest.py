import pytest
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from data.urls import Urls

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--log-level=3")  # Отключает внутренний мусорный лог Chrome updater/ipc
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Подавляет DevTools логи в консоли Windows
        driver = webdriver.Chrome(service=ChromeService(), options=options)
        
    elif request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(service=FirefoxService(), options=options)
        
    yield driver
    driver.quit()

@pytest.fixture
def create_user_and_auth(driver):
    # Генерация уникальных данных для нового тестового пользователя
    rand_id = random.randint(10000, 99999)
    payload = {
        "email": f"diplom3_user_{rand_id}@yandex.ru",
        "password": f"Password{rand_id}",
        "name": f"Tester_{rand_id}"
    }
    
    # Регистрация через API Stellar Burgers
    response = requests.post(Urls.API_CREATE_USER, json=payload)
    data = response.json()
    
    access_token = data.get("accessToken")   # Содержит строку "Bearer ..."
    refresh_token = data.get("refreshToken") # Необходим для полной инициализации сессии фронтенда
    
    # Открываем базовый URL, чтобы получить домен для записи в localStorage
    driver.get(Urls.BASE_URL)
    
    # Авторизуем пользователя, прокидывая ОБА токена напрямую в браузерную сессию
    driver.execute_script(f"localStorage.setItem('accessToken', '{access_token}');")
    driver.execute_script(f"localStorage.setItem('refreshToken', '{refresh_token}');")
    driver.refresh()
    
    yield payload
    
    # Очистка данных: обязательно удаляем созданного пользователя после завершения теста
    if access_token:
        requests.delete(Urls.API_DELETE_USER, headers={"Authorization": access_token})
