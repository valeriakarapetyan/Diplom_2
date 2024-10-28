import allure
import requests
import random
import string
from conftest import URL


@allure.epic("Тестирование POST /api/orders")
class TestCreateOrder:

    @allure.feature("Создание заказа авторизованным пользователем")
    @allure.title("Успешное создание заказа")
    def test_create_order_with_authorization(self, create_user, random_ingredients):
        email, password, name, access_token = create_user
        ingredients = random_ingredients

        response = requests.post(f"{URL}/api/orders", json={"ingredients": ingredients},
                                 headers={"Authorization": access_token})
        response_data = response.json()

        assert response.status_code == 200
        assert response_data.get("success") is True
        assert "order" in response_data
        assert "number" in response_data["order"]
        assert response_data["order"]["number"] > 0
        assert "_id" in response_data["order"]
        assert "owner" in response_data["order"]

    @allure.feature("Создание заказа неавторизованным пользователем")
    @allure.title("Успешное создание заказа")
    def test_create_order_without_authorization(self, random_ingredients):
        ingredients = random_ingredients

        response = requests.post(f"{URL}/api/orders", json={"ingredients": ingredients})
        response_data = response.json()

        assert response.status_code == 200
        assert response_data.get("success") is True
        assert "order" in response_data
        assert "number" in response_data["order"]
        assert response_data["order"]["number"] > 0

    @allure.feature("Создание заказа неавторизованным пользователем")
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        response = requests.post(f"{URL}/api/orders")

        assert response.status_code == 400
        assert response.json() == {
            "success": False,
            "message": "Ingredient ids must be provided"
        }

    @allure.feature("Создание заказа неавторизованным пользователем")
    @allure.title("Создание заказа с некорректными id")
    def test_create_order_with_wrong_hash(self):
        wrong_ingredient = []
        ingredient = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        wrong_ingredient.append(ingredient)

        response = requests.post(f"{URL}/api/orders", json={"ingredients": wrong_ingredient})

        assert response.status_code == 500
