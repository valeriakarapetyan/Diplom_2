import allure
import requests
from conftest import URL


@allure.epic("Тестирование POST /api/auth/login")
class TestLogin:

    @allure.feature("Авторизация под существующим пользователем")
    @allure.title("Успешная авторизация")
    def test_login_with_existing_user(self, create_user):
        email = create_user[0]
        password = create_user[1]
        name = create_user[2]

        response = requests.post(f"{URL}/api/auth/login", json={"email": email, "password": password})
        response_data = response.json()

        assert response.status_code == 200
        assert response_data.get("success") is True
        assert response_data["user"]["email"] == email
        assert response_data["user"]["name"] == name
        assert "accessToken" in response_data
        assert "refreshToken" in response_data

    @allure.feature("Авторизация несуществующего пользователя")
    @allure.title("Пароль или имейл некорректны")
    def test_login_with_non_existing_user(self, random_email, random_password):
        response = requests.post(f"{URL}/api/auth/login",
                                 json={"email": random_email, "password": random_password})

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "email or password are incorrect"
        }
