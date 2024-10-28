import allure
import requests
from conftest import URL


@allure.epic("Тестирование GET /api/orders")
class TestGetOrders:

    @allure.feature("Получение заказов")
    @allure.title("Авторизованный пользователь")
    def test_get_orders_authorized_user(self, create_orders):
        access_token = create_orders

        response = requests.get(f"{URL}/api/orders", headers={"Authorization": access_token})
        response_data = response.json()

        assert response.status_code == 200
        assert response_data.get("success") is True
        assert "orders" in response_data
        assert "total" in response_data
        assert "totalToday" in response_data

    @allure.feature("Получение заказов")
    @allure.title("Неавторизованный пользователь")
    def test_get_orders_non_authorized_user(self):
        response = requests.get(f"{URL}/api/orders")

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised"
        }
