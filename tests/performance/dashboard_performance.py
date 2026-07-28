import time
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/companies"

companies = ["ABB", "TCS", "INFY", "RELIANCE", "HDFCBANK"]

print("=" * 60)
print("Dashboard Performance Test")
print("=" * 60)

times = []

for company in companies:

    start = time.time()

    response = requests.get(f"{BASE_URL}/{company}")

    end = time.time()

    elapsed = end - start

    times.append(elapsed)

    print(f"{company:12} " f"Status={response.status_code} " f"Time={elapsed:.3f} sec")

print("=" * 60)

print("Average :", round(sum(times) / len(times), 3), "sec")

print("Maximum :", round(max(times), 3), "sec")

print("Minimum :", round(min(times), 3), "sec")

print("=" * 60)

if max(times) < 3:
    print("PASS : Dashboard performance target achieved")
else:
    print("FAIL : Dashboard slower than 3 seconds")
