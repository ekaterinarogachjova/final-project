import os
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from config.settings import BASE_URL, LOGIN, PASSWORD

@pytest.mark.ui
@allure.feature("Авторизация")
class TestAuthUI:

    def _close_popups(self, driver):
        wait = WebDriverWait(driver, 20)
        with allure.step("Закрываем popmechanic-попапы, если они появились"):
            try:
                no_thanks_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'button.popmechanic-btn.popmechanic-btn-second[data-popmechanic-close]')
                    )
                )
                no_thanks_btn.click()
            except TimeoutException:
                pass

            try:
                ok_btn = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'button.popmechanic-btn.popmechanic-btn-primary[data-popmechanic-close]')
                    )
                )
                ok_btn.click()
            except TimeoutException:
                pass

            try:
                close_icon = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'div.popmechanic-close[data-popmechanic-close]')
                    )
                )
                close_icon.click()
            except TimeoutException:
                pass

        with allure.step("Обрабатываем браузерные alert/confirm/prompt окна, если они появились"):
            try:
                alert = WebDriverWait(driver, 5).until(lambda d: d.switch_to.alert)
                alert_text = alert.text
                allure.attach(alert_text, name="Alert text", attachment_type=allure.attachment_type.TEXT)
                alert.accept()
            except (TimeoutException, NoAlertPresentException):
                pass

    @allure.title("Успешная авторизация на сайте")
    @allure.description("Проверяем, что пользователь может войти с валидными учетными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, driver):
        with allure.step("Открываем главную страницу"):
            driver.get(BASE_URL)

        self._close_popups(driver)

        with allure.step("Открываем форму авторизации"):
            # Если нужно, раскомментируйте и исправьте селекторы ниже:
            # driver.find_element(By.CSS_SELECTOR, ".user-icon").click()
            # driver.find_element(By.CSS_SELECTOR, ".user-menu-link.body_s").click()
            driver.find_element(By.XPATH, '//span[contains(@class, "is_text") and text()="Личный кабинет"]').click()

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
