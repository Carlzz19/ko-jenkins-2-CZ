import requests
from jsonschema import validate, ValidationError
from faker import Faker
import os
from dotenv import load_dotenv
import json
import allure

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://api-test.kelasotomesyen.com")
API_KEY = os.getenv("API_KEY", "")

AUTH_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "access_token": {"type": "string"},
        "token_type": {"type": "string"},
        "expires_in": {"type": "number"},
        "expires_at": {"type": "number"},
        "refresh_token": {"type": "string"},
        "user": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "email": {"type": "string"},
                "created_at": {"type": "string"}
            },
            "required": ["id", "email"]
        }
    },
    "required": ["access_token", "user"]
}

PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "price": {"type": ["number", "string"]},
        "stock": {"type": "number"},
        "category": {"type": "string", "enum": ["Electronics", "Clothing", "Food", "Books", "Home", "Sports", "Toys", "Other"]},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"}
    },
    "required": ["id", "name", "price", "stock", "category"]
}

# Global variables
fake = Faker()
test_access_token = None
test_product_id = None

@allure.epic("API Testing, Kelas Otomesyen")
@allure.feature("Autetikasi dan Manajemen Produk")
@allure.story("Test API dengan Credentials yang valid")
@allure.description("Test ini untuk memastikan bahhwa API dapat melakukan autentikasi pengguna dan membuat produk dengan benar.")
@allure.severity(allure.severity_level.CRITICAL)

# ==================== TEST AUTH ====================
def test_login_success():
    global test_access_token

    with allure.step("1. Menyiapkan payload utnuk login"):
        payload = {
            "email": "uno.testing3@gmail.com",
            "password": "1234567890"
        }

    with allure.step("2. Mengirim Post request ke endpoint authentication"):
        response = requests.post(
            f"{BASE_URL}/auth/v1/token?grant_type=password",
            json=payload,
            headers={"apikey": API_KEY}
        )

    with allure.step("3. Memvalidasi response dari server"):
        assert response.status_code == 200, f"Maunya 200 tapi malah dikasi {response.status_code}"
        allure.attach(str(response.status_code), name= "Status Code", attachment_type=allure.attachment_type.TEXT )

        data = response.json()
        validate(instance=data, schema=AUTH_RESPONSE_SCHEMA)
        allure.attach(response.text, name= "Response Body", attachment_type=allure.attachment_type.JSON)

        assert "access_token" in data
        assert data["expires_in"] == 3600
        allure.attach(str(data["expires_in"]), name= "Expires In", attachment_type=allure.attachment_type.TEXT)

        test_access_token = data["access_token"]
        allure.attach(data["access_token"], name= "Access Token", attachment_type=allure.attachment_type.TEXT)


# ====================TEST PRODUC ====================

def test_create_product_success():
    global test_product_id

    with allure.step("1. Menyiapkan data produk baru"):    
        params = {
        'columns': '"name","description","price","stock","category","user_id"',
        'select': '*'
        }

        product_data = {
            "name": fake.catch_phrase(),
            "description": fake.text(max_nb_chars=200),
            "price": round(fake.random_number(digits=5) / 100, 2),
            "stock": fake.random_int(min=1, max=100),
            "category": fake.random_element(elements=["Electronics", "Clothing", "Food", "Books", "Home", "Sports", "Toys", "Other"]),
            "user_id": "6d6738c8-cd99-4fce-82eb-0dd7069843b9"
        }

        headers = {
            "apikey": API_KEY,
            "Authorization": f"Bearer {test_access_token}",
            "Content-Type": "application/json",
            "prefer": "return=representation"
        }

    with allure.step("2. Mengirim Post request ke endpoint produk untuk membuat produk baru"):
        response = requests.post(
            f"{BASE_URL}/rest/v1/products",
            json=product_data,
            headers=headers, params=params
        )

        assert response.status_code == 201, f"Maunya 201 tapi malah dikasi {response.status_code}"
        allure.attach(str(response.status_code), name= "Status Code", attachment_type=allure.attachment_type.TEXT )

        data = response.json()
        print(data)
        assert isinstance(data, list), "Responsenya mestinya list/array"
        assert len(data) > 0, "Response list/array gak bole kosongan"

    with allure.step("3. Memvalidasi data produk yang dibuat"):
        product = data[0]
        validate(instance=product, schema=PRODUCT_SCHEMA)

        assert product["name"] == product_data["name"]
        assert product["category"] == product_data["category"]

        test_product_id = product["id"]
        allure.attach(product["id"], name= "Product ID", attachment_type=allure.attachment_type.TEXT)
