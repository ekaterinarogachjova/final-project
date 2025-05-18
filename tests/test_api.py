import os
import allure
import pytest
import requests
from config.settings import BASE_URL, LOGIN, PASSWORD

@pytest.mark.api
@allure.feature("Авторизация")
class TestAuthAPI:

    @allure.title("Авторизация с валидными учетными данными")
    @allure.description("Проверяем, что API возвращает токен при корректных данных")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_auth_with_valid_credentials(self):
        with allure.step("Формируем полезную нагрузку для запроса"):
            payload = {
                "login": LOGIN,
                "password": PASSWORD
            }

        with allure.step("Отправляем POST-запрос на эндпоинт авторизации"):
            response = requests.post(f"{BASE_URL}/api/v1/auth", json=payload)

        self._check_auth_success(response)

    @allure.step("Проверяем успешный ответ авторизации")
    def _check_auth_success(self, response):
        assert response.status_code == 200
        json_data = response.json()
        assert "token" in json_data
        assert len(json_data["token"]) > 30

    @allure.title("Авторизация с некорректными данными")
    @allure.description("Проверяем, что API возвращает ошибку при неверных данных")
    @allure.severity(allure.severity_level.NORMAL)
    def test_auth_with_invalid_data(self):
        with allure.step("Отправляем POST-запрос с некорректным логином"):
            response = requests.post(f"{BASE_URL}/api/v1/auth", json={"login": "test"})

        self._check_auth_failure(response)

    @allure.step("Проверяем ответ с ошибкой авторизации")
    def _check_auth_failure(self, response):
        assert response.status_code == 400
        assert "validation error" in response.text.lower()

@pytest.mark.api
@allure.feature("Поиск туров")
class TestTourAPI:

    @allure.title("Поиск туров через API с валидными параметрами")
    @allure.description("Проверяем, что API возвращает список туров по заданным параметрам")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_endpoint(self):
        with allure.step("Формируем параметры запроса"):
            params = {
                "destination": "Antalya",
                "checkin": "2025-09-01",
                "duration": 7
            }

        with allure.step("Отправляем GET-запрос на поиск туров"):
            response = requests.get(f"{BASE_URL}/api/v1/tours", params=params)

        self._check_search_response(response)

    @allure.step("Проверяем корректность ответа поиска туров")
    def _check_search_response(self, response):
        assert response.status_code == 200
        json_data = response.json()
        assert isinstance(json_data.get("results"), list)

    @allure.title("Получение деталей тура по ID")
    @allure.description("Проверяем, что API возвращает корректные данные тура по идентификатору")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tour_details(self):
        with allure.step("Отправляем GET-запрос на получение деталей тура"):
            response = requests.get(f"{BASE_URL}/api/v1/tours/123")

        self._check_tour_details(response)

    @allure.step("Проверяем структуру данных тура")
    def _check_tour_details(self, response):
        assert response.status_code == 200
        json_data = response.json()
        for key in ["title", "price", "duration"]:
            assert key in json_data