import json
import requests
from datetime import datetime

with open("token.json") as f:
    data = json.load(f)

url = "http://iot.jowinwin.com/oauth2/token.php"
body = {
    "grant_type":"refresh_token",
    "refresh_token": data["refresh_token"]
}
headers = {
    "Authorization":"Basic VERTY2xpZW50OlREU3Bhc3M="
}

r = requests.post(url, data=body, headers=headers)
data = r.json()
# add number of seconds from current time at my timezone to 1970-01-01 UTC
data['time_stamp'] = datetime.now().timestamp()
print(data)

with open("token.json", 'w', encoding="utf-8") as f:
    # f.write(f"{datetime.now()}\n")
    json.dump(data, f, ensure_ascii=False, indent=4)
