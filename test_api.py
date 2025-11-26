import requests
import allure

BASE_URL = "https://hluyxndmpmooyznhfwxc.supabase.co"
PRODUCTS_ENDPOINT = "/rest/v1/products"

AUTH = "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6ImRIWis2SmtoMUxhMlpQMXgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2hsdXl4bmRtcG1vb3l6bmhmd3hjLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI3NDlkMjZmYy1mZTA0LTQ5YTItYWZmNS0yYzFkMTlmNzllYjciLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzYzODkxODIyLCJpYXQiOjE3NjM4ODgyMjIsImVtYWlsIjoidW5vLnRlc3RpbmczQGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWwiOiJ1bm8udGVzdGluZzNAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwic3ViIjoiNzQ5ZDI2ZmMtZmUwNC00OWEyLWFmZjUtMmMxZDE5Zjc5ZWI3In0sInJvbGUiOiJhdXRoZW50aWNhdGVkIiwiYWFsIjoiYWFsMSIsImFtciI6W3sibWV0aG9kIjoicGFzc3dvcmQiLCJ0aW1lc3RhbXAiOjE3NjM3MzUwODl9XSwic2Vzc2lvbl9pZCI6ImZiM2ZjYzk5LWVjMDktNGFlOC1iNTc5LWE1MmE3MjljMjVkYyIsImlzX2Fub255bW91cyI6ZmFsc2V9.1jBMlJu-_Ar8uyJI41xRkueuPaTNru-QTs8MHOZVHNQ"

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsdXl4bmRtcG1vb3l6bmhmd3hjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2ODQ4MTQsImV4cCI6MjA2NTI2MDgxNH0.lVhUKhscl3nT6oeVbnXb0BbF0mI0lFR_KKlxYMX6Mnc"

HEADERS = {
    "Apikey": API_KEY,
    "Authorization": AUTH
}

PARAMS = {
    "select": "*",
    "order": "created_at.desc"
}

@allure.feature("Products API")
@allure.story("Get Product List")
@allure.title("Get Product List Hepi flow dah")
@allure.description("Memastikan GET /products mengembalikan daftar produk dengan response 200 dan struktur JSON yang valid.")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_product_list():

    url = BASE_URL + PRODUCTS_ENDPOINT

    with allure.step(f"Kirim request GET ke {url} pake params {PARAMS}"):
        resp = requests.get(url, headers=HEADERS, params=PARAMS)

    with allure.step("Validasi status code 200"):
        assert resp.status_code == 201, f"Expected 200 got {resp.status_code}"

    with allure.step("Parse JSON response"):
        json_data = resp.json()

    with allure.step("Validasi bahwa response adalah list data"):
        assert isinstance(json_data, list), "Response harus berupa list"

    if json_data:
        with allure.step("Validasi structure field produk paling minim"):
            sample = json_data[0]
            assert "id" in sample, "Field `id` tidak ditemukan"
            assert "name" in sample, "Field `name` tidak ditemukan"
            assert "created_at" in sample, "Field `created_at` tidak ditemukan"


