import json
import requests

access_token = "3ca023a32a2249a00fa8282a0686e30acdb8cfd5"
url = "https://iot.jowinwin.com/iot_tds/control.php"
body = {
    "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
    "inputs": [
        {
            "intent": "action.devices.QUERY",
            "payload": {
                "devices": [
                    {
                        "id": "a00abf1dd7e7",
                        "customData": {
                        }
                    },
                    {
                        "id": "a00abf1ddb09",
                        "customData": {
                        }
                    },
                    {
                        "id": "a00abf1ddb37",
                        "customData": {
                        }
                    },
                    {
                        "id": "a00abf394b1c",
                        "customData": {
                        }
                    }
                ]
            }
        }
    ]
}
headers = {"Authorization": "Bearer " + access_token}
r = requests.post(url, data=json.dumps(body), headers=headers)

# - Fan
fan_id = "a00abf394b1c"
fan_on = None  # True, False
fan_speed = None  # int
# - A/C
ac_id = "a00abf1dd7e7"
ac_on = None  # True, False
ac_set_temp = None  # int
ac_ambient_temp = None  # int 
# - A/F
af_id = "a00abf1ddb09"
af_on = None  # True, False
af_pm25 = None  # float

r_dict = r.json()
for device in r_dict["payload"]["devices"]:
    if fan_id in device.keys():
        fan_on = device[fan_id]["on"]
        fan_speed = device[fan_id]["currentFanSpeedSetting"]
    elif ac_id in device.keys():
        ac_on = device[ac_id]["on"]
        ac_set_temp = device[ac_id]["thermostatTemperatureSetpoint"]
        ac_ambient_temp = device[ac_id]["thermostatTemperatureAmbient"]
    elif af_id in device.keys():
        af_on = device[af_id]["on"]
        af_pm25 = device[af_id]["currentSensorStateData"][0]["rawValue"]
    else:
        print(f"Unknown device: {device.keys()}")

print(fan_on, fan_speed, ac_on, ac_set_temp, ac_ambient_temp, af_on, af_pm25)