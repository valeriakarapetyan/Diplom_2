import allure
import requests
from conftest import URL


@allure.epic("Тестирование PATCH /api/auth/user")
class TestChangeUser:

    @allure.feature("Изменение пользователя без авторизации")
    @allure.title("Изменение name")
    def test_change_name_without_authorization(self, random_name):
        new_name = random_name

        response = requests.patch(f"{URL}/api/auth/user",
                                  json={"name": new_name})

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised"
        }

    @allure.feature("Изменение пользователя без авторизации")
    @allure.title("Изменение password")
    def test_change_password_without_authorization(self, random_password):
        new_password = random_password

        response = requests.patch(f"{URL}/api/auth/user",
                                  json={"password": new_password})

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised"
        }

    @allure.feature("Изменение пользователя без авторизации")
    @allure.title("Изменение email")
    def test_change_email_without_authorization(self, random_email):
        new_email = random_email

        response = requests.patch(f"{URL}/api/auth/user",
                                  json={"email": new_email})

        assert response.status_code == 401
        assert response.json() == {
            "success": False,
            "message": "You should be authorised"
        }

    @allure.feature("Изменение пользователя с авторизацией")
    @allure.title("Изменение email")
    def test_change_email_with_authorization(self, create_user, random_email):
        email, password, name, access_token = create_user
        new_email = random_email

        response = requests.patch(f"{URL}/api/auth/user",
                                  json={"email": new_email},
                                  headers={"Authorization": access_token})

        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "user": {
                "email": new_email,
                "name": name
            }
        }

    @allure.feature("Изменение пользователя с авторизацией")
    @allure.title("Изменение password")
    def test_change_password_with_authorization(self, create_user, random_password):
        email, password, name, access_token = create_user
        new_password = random_password

        response = requests.patch(f"{URL}/api/auth/user",
                                  json={"password": new_password},
                                  headers={"Authorization": access_token})

        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "user": {
                "email": email,
                "name": name
            }
        }

    @allure.feature("Изменение пользователя с авторизацией")
    @allure.title("Изменение name")
    def test_change_name_with_authorization(self, create_user, random_name):
        email, password, name, access_token = create_user
        new_name = random_name

        response = requests.patch(f"{URL}/api/auth/user",
                                  json={"password": new_name},
                                  headers={"Authorization": access_token})

        assert response.status_code == 200
        assert response.json() == {
            "success": True,
            "user": {
                "email": email,
                "name": new_name
            }
        }
