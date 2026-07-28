import threading
import time
import requests

URL = "http://127.0.0.1:8000/api/v1/screener"

times = []


def call_api():

    start = time.time()

    response = requests.get(URL)

    end = time.time()

    print(f"Status: {response.status_code} | " f"{end-start:.3f} sec")

    times.append(end - start)


threads = []

overall_start = time.time()

for _ in range(10):

    t = threading.Thread(target=call_api)

    threads.append(t)

    t.start()

for t in threads:
    t.join()

overall_end = time.time()

print("=" * 60)
print("TOTAL REQUESTS :", len(times))
print("TOTAL TIME     :", round(overall_end - overall_start, 3), "seconds")
print("AVERAGE TIME   :", round(sum(times) / len(times), 3), "seconds")
print("MAX TIME       :", round(max(times), 3), "seconds")
print("=" * 60)
