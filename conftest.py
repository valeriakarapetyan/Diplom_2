import pytest
import random
import string

import requests

URL = 'https://stellarburgers.nomoreparties.site'


@pytest.fixture
def random_email():
    suffix = "@example.com"
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return random_string + suffix


@pytest.fixture
def random_password():
    return "".join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=8))


@pytest.fixture
def random_name():
    return "User_" + "".join(random.choices(string.ascii_letters, k=5))


@pytest.fixture
def create_user(random_email, random_password, random_name):
    email = random_email
    password = random_password
    name = random_name

    response = requests.post(f"{URL}/api/auth/register", json={"email": email, "password": password, "name": name})
    access_token = response.json()["accessToken"]

    yield email, password, name, access_token

    requests.delete(f"{URL}/auth/user", json={"email": email},
                    headers={"Authorization": access_token})


@pytest.fixture
def random_ingredients():
    response = requests.get(f"{URL}/api/ingredients")
    ingredients = response.json()["data"]
    # выбираю два рандомных ингредиента для упрощения теста
    chosen_ingredients = random.sample([ingredient["_id"] for ingredient in ingredients], 2)
    return chosen_ingredients


@pytest.fixture
def create_orders(create_user, random_ingredients):
    email, password, name, access_token = create_user
    ingredients = random_ingredients
    requests.post(f"{URL}/api/orders", json={"ingredients": ingredients},
                  headers={"Authorization": access_token})
    return access_token
