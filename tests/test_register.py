import allure
import requests
from conftest import URL


@allure.epic("Тестирование POST /api/auth/register")
class TestRegister:

    @allure.feature("Регистрация нового пользователя")
    @allure.title("Успешная регистрация")
    def test_create_new_user(self, random_email, random_password, random_name):
        email = random_email
        password = random_password
        name = random_name

        response = requests.post(f"{URL}/api/auth/register", json={"email": email, "password": password, "name": name})
        response_data = response.json()

        assert response.status_code == 200
        assert response_data.get("success") is True
        assert response_data["user"]["email"] == email
        assert response_data["user"]["name"] == name
        assert "accessToken" in response_data
        assert "refreshToken" in response_data

    @allure.feature("Повторная регистрация пользователя")
    @allure.title("Пользователь уже существует")
    def test_create_existing_user(self, create_user):
        email = create_user[0]
        password = create_user[1]
        name = create_user[2]

        response = requests.post(f"{URL}/api/auth/register", json={"email": email, "password": password, "name": name})

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "User already exists"
        }

    @allure.feature("Регистрация нового пользователя")
    @allure.title("Регистрация без email")
    def test_create_user_without_email(self):
        response = requests.post(f"{URL}/api/auth/register",
                                 json={"email": None, "password": "password", "name": "Username"})

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields"
        }

    @allure.feature("Регистрация нового пользователя")
    @allure.title("Регистрация без password")
    def test_create_user_without_password(self):
        response = requests.post(f"{URL}/api/auth/register",
                                 json={"email": "test@yandex.ru", "password": None, "name": "Username"})

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields"
        }

    @allure.feature("Регистрация нового пользователя")
    @allure.title("Регистрация без name")
    def test_create_user_without_name(self):
        response = requests.post(f"{URL}/api/auth/register",
                                 json={"email": "test@yandex.ru", "password": "password", "name": None})

        assert response.status_code == 403
        assert response.json() == {
            "success": False,
            "message": "Email, password and name are required fields"
        }
