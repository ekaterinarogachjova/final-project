import os
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import BASE_URL, LOGIN, PASSWORD

@pytest.mark.ui
@allure.feature("Авторизация")
class TestAuthUI:

    @allure.title("Успешная авторизация на сайте")
    @allure.description("Проверяем, что пользователь может войти с валидными учетными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        with allure.step("Открываем главную страницу"):
            driver.get(BASE_URL)
        with allure.step("Удаляем всплывающие окна через JS"):
             driver.execute_script("document.querySelectorAll('.popup, .modal').forEach(e => e.remove())")
        with allure.step("Открываем форму авторизации"):
            wait = WebDriverWait(driver, 15)
            element = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//span[contains(@class, "is_text") and text()="Личный кабинет"]')
                )
            )
            try:
                element.click()
            except Exception:
                # Если обычный клик не сработал, используем JS-клик
                driver.execute_script("arguments[0].click();", element)
        
        
        
        
        
        
        
        #with allure.step("Открываем форму авторизации"):
        # driver.find_element(By.CSS_SELECTOR, ".user-icon").click()
        # driver.find_element(By.CSS_SELECTOR, ".user-menu-link.body_s").click()
        #driver.find_element(By.XPATH, '//span[contains(@class, "is_text") and text()="Личный кабинет"]').click()

        with allure.step("Вводим логин и пароль"):
            driver.find_element(By.NAME, "login").send_keys(LOGIN)
            driver.find_element(By.NAME, "password").send_keys(PASSWORD)

        with allure.step("Нажимаем кнопку Войти"):
            driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()

        self._check_login_success(driver)

    @allure.step("Проверяем успешный вход в личный кабинет")
    def _check_login_success(self, driver):
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Личный кабинет")
        )
        assert "Личный кабинет" in driver.page_source

    @allure.title("Авторизация с неверными данными")
    @allure.description("Проверяем, что при неверном логине или пароле отображается ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_credentials(self, driver):
        with allure.step("Открываем главную страницу"):
            driver.get(BASE_URL)

        with allure.step("Открываем форму авторизации"):
            driver.find_element(By.CSS_SELECTOR, ".user-icon").click()

        with allure.step("Вводим неверные логин и пароль"):
            driver.find_element(By.NAME, "login").send_keys("wrong@email.com")
            driver.find_element(By.NAME, "password").send_keys("invalid")

        with allure.step("Нажимаем кнопку Войти"):
            driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()

        self._check_login_error(driver)

    @allure.step("Проверяем отображение ошибки авторизации")
    def _check_login_error(self, driver):
        error_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
        )
        assert "неверный логин или пароль" in error_element.text.lower()

@pytest.mark.ui
@allure.feature("Поиск туров")
class TestTourSearchUI:

    @allure.title("Поиск туров с валидными параметрами")
    @allure.description("Проверяем, что поиск туров по фильтрам возвращает результаты")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tour_search_by_filters(self, driver):
        with allure.step("Открываем главную страницу"):
            driver.get(BASE_URL)

        with allure.step("Вводим параметры поиска"):
            driver.find_element(By.ID, "search-destination").send_keys("Турция")
            driver.find_element(By.ID, "search-checkin").send_keys("01.09.2025")
            duration_input = driver.find_element(By.ID, "search-duration")
            duration_input.clear()
            duration_input.send_keys("7")

        with allure.step("Запускаем поиск"):
            driver.find_element(By.CSS_SELECTOR, ".search-button").click()

        with allure.step("Ожидаем появления результатов"):
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tour-card"))
            )

        with allure.step("Проверяем, что найдено минимум 3 тура"):
            results = driver.find_elements(By.CLASS_NAME, "tour-card")
            assert len(results) >= 3

    @allure.title("Поиск туров с отсутствующими результатами")
    @allure.description("Проверяем, что при поиске по несуществующему направлению отображается сообщение об отсутствии результатов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_search_results(self, driver):
        with allure.step("Открываем главную страницу"):
            driver.get(BASE_URL)

        with allure.step("Вводим несуществующее направление"):
            driver.find_element(By.ID, "search-destination").send_keys("Марс")

        with allure.step("Запускаем поиск"):
            driver.find_element(By.CSS_SELECTOR, ".search-button").click()

        with allure.step("Ожидаем сообщение об отсутствии результатов"):
            message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "empty-results"))
            ).text

        with allure.step("Проверяем текст сообщения"):
            assert "ничего не найдено" in message.lower()