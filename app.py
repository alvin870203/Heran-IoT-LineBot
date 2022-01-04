# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.


import os
import sys
import json
import requests
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

access_token = os.getenv('access_token', None)  # token for IoT appliances
url = "https://iot.jowinwin.com/iot_tds/control.php"  # url for appliances' control
headers = {"Authorization": "Bearer " + access_token}  # OAuth2.0 url for appliances' control

# State of the devices
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


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        update_devces_state()        
        
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):  # text message
            text = event.message.text
            if text == "測試":
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text=event.message.text),
                        ImageSendMessage(
                            original_content_url="https://serene-stream-27454.herokuapp.com/static/test.png",
                            preview_image_url="https://serene-stream-27454.herokuapp.com/static/test.png"
                        )
                    ]
                )
            elif text == "電風扇":
                buttons_message_fan = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/電風扇.jpg',
                        image_aspect_ratio='rectangle',
                        image_size='contain',
                        title='Menu',
                        text='Please select',
                        actions=[
                            PostbackAction(
                                label='開機/關機',
                                # display_text='postback text',
                                data='fan_onoff'
                            ),
                            PostbackAction(
                                label='增強風量',
                                # display_text='postback text',
                                data='fan_speed_up'
                            ),
                            PostbackAction(
                                label='降低風量',
                                # display_text='postback text',
                                data='fan_speed_down'
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(
                    event.reply_token, [buttons_message_fan]
                )
            elif text == "掃地機":
                buttons_message_vacuum = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/掃地機.jpg',
                        image_aspect_ratio='rectangle',
                        image_size='contain',
                        title='Menu',
                        text='Please select',
                        actions=[
                            PostbackAction(
                                label='開機/關機',
                                # display_text='postback text',
                                data='vacuum_onoff'
                            ),
                        ]
                    )
                )
                line_bot_api.reply_message(
                    event.reply_token, [buttons_message_vacuum]
                )
            elif text == "冷氣":
                buttons_message_ac = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/冷氣.jpg',
                        image_aspect_ratio='rectangle',
                        image_size='contain',
                        title='Menu',
                        text='Please select',
                        actions=[
                            PostbackAction(
                                label='開機/關機',
                                # display_text='postback text',
                                data='ac_onoff'
                            ),
                            PostbackAction(
                                label='溫度升',
                                # display_text='postback text',
                                data='ac_temp_up'
                            ),
                            PostbackAction(
                                label='溫度降',
                                # display_text='postback text',
                                data='ac_temp_down'
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(
                    event.reply_token, [buttons_message_ac]
                )
            elif text == "空氣清淨機":
                buttons_message_af = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/空氣清淨機.jpg',
                        image_aspect_ratio='rectangle',
                        image_size='contain',
                        title='Menu',
                        text='Please select',
                        actions=[
                            PostbackAction(
                                label='開機/關機',
                                # display_text='postback text',
                                data='af_onoff'
                            ),
                        ]
                    )
                )
                line_bot_api.reply_message(
                    event.reply_token, [buttons_message_af]
                )
            elif text == "除濕機":
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text="尚未配對"+text)]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text="無此功能")]
                )
        elif isinstance(event, PostbackEvent):  # postback event
            data = event.postback.data
            if data == "fan_onoff":
                fan_on_off()
        
        
    return 'OK'


def update_devces_state():
    global fan_on, fan_speed, ac_on, ac_set_temp, ac_ambient_temp, af_on, af_pm25
    body = {
        "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
        "inputs": [{
            "intent": "action.devices.QUERY",
            "payload": {
                "devices": [
                    {"id": ac_id},  # A/C
                    {"id": af_id},  # A/F
                    {"id": fan_id}   # fan
                ]
            }
        }]
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)
    r_dict = r.json()
    print(r_dict)
    for device in r_dict["payload"]["devices"]:
        if fan_id in device.keys():
            fan_on = bool(device[fan_id]["on"])
            fan_speed = int(device[fan_id]["currentFanSpeedSetting"])
            print(f"Update fan: {fan_on=}, {fan_speed=}")
        elif ac_id in device.keys():
            ac_on = bool(device[ac_id]["on"])
            ac_set_temp = int(device[ac_id]["thermostatTemperatureSetpoint"])
            ac_ambient_temp = int(device[ac_id]["thermostatTemperatureAmbient"])
            print(f"Update ac: {ac_on=}, {ac_set_temp=}, {ac_ambient_temp=}")
        elif af_id in device.keys():
            af_on = bool(device[af_id]["on"])
            af_pm25 = float(device[af_id]["currentSensorStateData"][0]["rawValue"])  #FIXME: float or int ?
            print(f"Update af: {af_on=}, {af_pm25=}")
        else:
            print(f"Unknown device: {device.keys()}")


def fan_on_off():
    if fan_on is True:
        body = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "inputs": [{
                "intent": "action.devices.EXECUTE",
                "payload": {
                    "commands": [{
                        "devices": [{
                            "id": "a00abf394b1c"
                        }],
                        "execution": [{
                            "command": "action.devices.commands.OnOff",
                            "params": {"on": False}
                        }]
                    }]
                }
            }]
        }
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
    elif fan_on is False:
        body = {
            "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
            "inputs": [{
                "intent": "action.devices.EXECUTE",
                "payload": {
                    "commands": [{
                        "devices": [{
                            "id": "a00abf394b1c"
                        }],
                        "execution": [{
                            "command": "action.devices.commands.OnOff",
                            "params": {"on": True}
                        }]
                    }]
                }
            }]
        }
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
    else:
        print(f"ERROR: wrong fan_on value = {fan_on}")


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
