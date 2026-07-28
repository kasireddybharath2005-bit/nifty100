import requests

FASTAPI_URL = "http://127.0.0.1:8000"
STREAMLIT_URL = "http://127.0.0.1:8501"

print("=" * 60)
print("END TO END INTEGRATION TEST")
print("=" * 60)

# -------------------------
# FastAPI Check
# -------------------------

try:
    response = requests.get(FASTAPI_URL)

    print(f"FastAPI : {response.status_code}")

except Exception as e:

    print("FastAPI Failed")

    print(e)

# -------------------------
# Streamlit Check
# -------------------------

try:
    response = requests.get(STREAMLIT_URL)

    print(f"Streamlit : {response.status_code}")

except Exception as e:

    print("Streamlit Failed")

    print(e)

# -------------------------
# API Endpoint Check
# -------------------------

try:

    response = requests.get(FASTAPI_URL + "/api/v1/companies")

    if response.status_code == 200:

        data = response.json()

        print("Companies Loaded :", len(data["companies"]))

except Exception as e:

    print(e)

print("=" * 60)
print("Integration Test Completed")
print("=" * 60)
