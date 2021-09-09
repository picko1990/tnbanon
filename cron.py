import time
import requests


if __name__ == '__main__':
    count = 1
    while True:
        try:
            requests.get("http://127.0.0.1:8000/cron/")
            print(f"cron got run {count} times")
            count += 1
        except requests.exceptions.ConnectionError:
            print("make sure the server is running")
        time.sleep(60)
