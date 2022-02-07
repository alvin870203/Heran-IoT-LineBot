import json
import requests
# from datetime import datetime

url = "http://iot.jowinwin.com/oauth2/token.php"
body = {
    "grant_type":"authorization_code",
    "code":"f6ed20eb2be557a7b7dfac8da29ffc5d68b628f7"
}
headers = {
    "Authorization":"Basic VERTY2xpZW50OlREU3Bhc3M="
}

r = requests.post(url, data=body, headers=headers)
data = r.json()
print(data)

with open("token.json", 'w', encoding="utf-8") as f:
    # f.write(f"{datetime.now()}\n")
    json.dump(data, f, ensure_ascii=False, indent=4)
