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

import pymongo
from bson.objectid import ObjectId

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
fan_speed = -1  # int
fan_turn = None  # True, False
# - A/C
ac_id = "a00abf1dd7e7"
ac_on = None  # True, False
ac_set_temp = -1  # int
ac_ambient_temp = -1  # int 
# - A/F
af_id = "a00abf1ddb09"
af_on = None  # True, False
af_pm25 = -1.  # float
# - vacuum
vacuum_id = "54752861b4e62d526cdb"
vacuum_on = None  # True, False

#FIXME: what's the init tab?
current_tab = "scenario"  # {scenario, living_room, master_bedroom, elder_bedroom}

# State of the scenario setting
scenarios_on_off = {
    "go_home_on": ["ac_box", "add_box_on"],
    "go_home_off": ["af_box", "vacuum_box", "add_box_off"],
    "all_go_out_on": ["add_box_on"],
    "all_go_out_off": ["ac_box", "fan_box", "af_box", "vacuum_box", "add_box_off"],
    "go_out_on": ["af_box", "vacuum_box", "add_box_on"],
    "go_out_off": ["ac_box", "add_box_off"],
    "night_on": ["add_box_on"],
    "night_off": ["add_box_off"],
    "morning_on": ["add_box_on"],
    "morning_off": ["add_box_off"],
    "noon_on": ["add_box_on"],
    "noon_off": ["add_box_off"]
}

scenarios_settings = {
    
    "go_home": {"speed": 3, "turn": False, "temp": 25},
    "all_go_out": {"speed": 4, "turn": False, "temp": 28},
    "go_out": {"speed": 5, "turn": False, "temp": 28},
    "night": {"speed": 6, "turn": False, "temp": 27},
    "morning": {"speed": 7, "turn": False, "temp": 26},
    "noon": {"speed": 8, "turn": False, "temp": 22},
}

# re-new a document on MongoDB
cluster = "mongodb+srv://alvin870203:Lmjh990231@cluster0.5iust.mongodb.net/line_bot?retryWrites=true&w=majority"
client = pymongo.MongoClient(cluster)
print(client.list_database_names())
db = client.line_bot
print(db.list_collection_names())
states = db.states
def get_state0():
    state0 = {
        "fan_on": fan_on,
        "fan_speed": fan_speed,
        "fan_turn": fan_turn,
        "ac_on": ac_on,
        "ac_set_temp": ac_set_temp,
        "ac_ambient_temp": ac_ambient_temp,
        "af_on": af_on,
        "af_pm25": af_pm25,
        "vacuum_on": vacuum_on,
        "current_tab": current_tab,
        "scenarios_on_off": scenarios_on_off,
        "scenarios_settings": scenarios_settings
    }
    return state0
object_id_dict = {"_id": ObjectId("61d7363db23cc7cb5c674635")}
result = states.replace_one(object_id_dict, get_state0())
print(f"MongoDB: {result=}")


def get_boxes(scenario):
    # device's components for scenario setting
    boxes = {
        "ac_box": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "冷氣",
                    "align": "center",
                    "size": "md",
                    "offsetTop": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": f"{'on' if ac_on is True else 'off'} / {scenarios_settings[scenario]['temp']}°C",
                    "size": "sm",
                    "color": "#888888",
                    "align": "center",
                    "offsetTop": "sm"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#dcdede"
                },
                {
                    "type": "image",
                    "url": "https://serene-stream-27454.herokuapp.com/static/ac.png",
                    "aspectMode": "fit",
                    "aspectRatio": "1.5:1",
                    "action": {
                        "type": "postback",
                        "data": f"adjust_ac_{scenario}"
                    }
                },
                {
                    "type": "image",
                    "url": "https://serene-stream-27454.herokuapp.com/static/remove.png",
                    "size": "18px",
                    "position": "absolute",
                    "offsetTop": "2px",
                    "offsetEnd": "2px",
                    "action": {
                        "type": "postback",
                        "data": f"remove_ac_{scenario}"
                    }
                },
                {
                    "type": "image",
                    "url": "https://placeholder.com/512",
                    "size": "36px",
                    "position": "absolute",
                    "offsetEnd": "none",
                    "action": {
                        "type": "postback",
                        "data": f"remove_ac_{scenario}"
                    },
                    "offsetTop": "none"
                }
            ],
            "borderColor": "#888888",
            "borderWidth": "medium",
            "cornerRadius": "md",
            "backgroundColor": "#FFFFFFcc"
        },

        "fan_box": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "電扇",
                    "align": "center",
                    "size": "md",
                    "offsetTop": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": f"{'on' if fan_on is True else 'off'} / 風速 {scenarios_settings[scenario]['speed']} / {'擺頭' if scenarios_settings[scenario]['turn'] is True else '固定'}",
                    "size": "sm",
                    "color": "#888888",
                    "align": "center",
                    "offsetTop": "sm"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#dcdede"
                },
                {
                    "type": "image",
                    "url": "https://serene-stream-27454.herokuapp.com/static/fan.png",
                    "aspectMode": "fit",
                    "aspectRatio": "1.5:1",
                    "action": {
                        "type": "postback",
                        "data": f"adjust_fan_{scenario}"
                    }
                },
                {
                    "type": "image",
                    "url": "https://serene-stream-27454.herokuapp.com/static/remove.png",
                    "size": "18px",
                    "position": "absolute",
                    "offsetTop": "2px",
                    "offsetEnd": "2px",
                    "action": {
                        "type": "postback",
                        "data": f"remove_fan_{scenario}"
                    }
                },
                {
                    "type": "image",
                    "url": "https://placeholder.com/512",
                    "size": "36px",
                    "position": "absolute",
                    "offsetEnd": "none",
                    "action": {
                        "type": "postback",
                        "data": f"remove_fan_{scenario}"
                    },
                    "offsetTop": "none"
                }
            ],
            "borderColor": "#888888",
            "borderWidth": "medium",
            "cornerRadius": "md",
            "backgroundColor": "#FFFFFFcc"
        },

        "add_box_on": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "新增",
                    "align": "center",
                    "size": "md",
                    "offsetTop": "md",
                    "weight": "bold"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#dcdede"
                },
                {
                    "type": "text",
                    "text": "+",
                    "size": "4xl",
                    "color": "#4265b4",
                    "weight": "bold",
                    "align": "center",
                    "gravity": "center"
                }
            ],
            "borderColor": "#888888",
            "borderWidth": "medium",
            "cornerRadius": "md",
            "backgroundColor": "#FFFFFFcc",
            "action": {
                "type": "postback",
                "data": f"add_on_{scenario}"
            }
        },

        "add_box_off": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "新增",
                    "align": "center",
                    "size": "md",
                    "offsetTop": "md",
                    "weight": "bold"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#dcdede"
                },
                {
                    "type": "text",
                    "text": "+",
                    "size": "4xl",
                    "color": "#4265b4",
                    "weight": "bold",
                    "align": "center",
                    "gravity": "center"
                }
            ],
            "borderColor": "#888888",
            "borderWidth": "medium",
            "cornerRadius": "md",
            "backgroundColor": "#FFFFFFcc",
            "action": {
                "type": "postback",
                "data": f"add_off_{scenario}"
            }
        },

        "af_box": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "清淨機",
                    "align": "center",
                    "size": "md",
                    "offsetTop": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": f"{'on' if af_on is True else 'off'} / {int(af_pm25)} PM2.5",
                    "size": "sm",
                    "color": "#888888",
                    "align": "center",
                    "offsetTop": "sm"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#dcdede"
                },
                {
                    "type": "image",
                    "url": "https://serene-stream-27454.herokuapp.com/static/af.png",
                    "aspectMode": "fit",
                    "aspectRatio": "1.5:1"
                },
                {
                    "type": "image",
                    "url": "https://serene-stream-27454.herokuapp.com/static/remove.png",
                    "size": "18px",
                    "position": "absolute",
                    "offsetTop": "2px",
                    "offsetEnd": "2px",
                    "action": {
                        "type": "postback",
                        "data": f"remove_af_{scenario}"
                    }
                },
                {
                    "type": "image",
                    "url": "https://placeholder.com/512",
                    "size": "36px",
                    "position": "absolute",
                    "offsetEnd": "none",
                    "action": {
                        "type": "postback",
                        "data": f"remove_af_{scenario}"
                    },
                    "offsetTop": "none"
                }
            ],
            "borderColor": "#888888",
            "borderWidth": "medium",
            "cornerRadius": "md",
            "backgroundColor": "#FFFFFFcc"
        },

        "vacuum_box": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "掃地機",
                    "align": "center",
                    "size": "md",
                    "offsetTop": "md",
                    "weight": "bold"
                },
                {
                    "type": "text",
                    "text": f"{'on / 清掃中' if vacuum_on is True else 'off / 充電中'}",
                    "size": "sm",
                    "color": "#888888",
                    "align": "center",
                    "offsetTop": "sm"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#dcdede"
                },
                {
                    "type": "image",
                    "url": "https://serene-stream-27454.herokuapp.com/static/vacuum.png",
                    "aspectMode": "fit",
                    "aspectRatio": "1.5:1"
                },
                {
                    "type": "image",
                    "url": "https://serene-stream-27454.herokuapp.com/static/remove.png",
                    "size": "18px",
                    "position": "absolute",
                    "offsetTop": "2px",
                    "offsetEnd": "2px",
                    "action": {
                        "type": "postback",
                        "label": "action",
                        "data": f"remove_vacuum_{scenario}"
                    }
                },
                {
                    "type": "image",
                    "url": "https://placeholder.com/512",
                    "size": "36px",
                    "position": "absolute",
                    "offsetEnd": "none",
                    "action": {
                        "type": "postback",
                        "data": f"remove_vacuum_{scenario}"
                    },
                    "offsetTop": "none"
                }
            ],
            "borderColor": "#888888",
            "borderWidth": "medium",
            "cornerRadius": "md",
            "backgroundColor": "#FFFFFFcc"
        }
    }
    return boxes

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
        load_database()  # load global variables states from MongoDB
        update_devices_state()
        
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
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/fan_white.jpg',
                        image_aspect_ratio='rectangle',
                        image_size='contain',
                        title='電風扇控制介面',
                        text=f"裝置狀態: {'開' if fan_on is True else '關'} / 風速: {fan_speed} / 風向: {'擺頭' if fan_turn is True else '固定'}",
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
                            ),
                            PostbackAction(
                                label='固定/擺頭',
                                # display_text='postback text',
                                data='fan_turn_toggle'
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
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/vacuum_white.jpg',
                        image_aspect_ratio='rectangle',
                        image_size='contain',
                        title='掃地機控制介面',
                        text=f"裝置狀態: {'清掃中' if vacuum_on is True else '已回家充電'}",
                        actions=[
                            PostbackAction(
                                label='回家充電/開始清掃',
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
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/ac_white.jpg',
                        image_aspect_ratio='rectangle',
                        image_size='contain',
                        title='冷氣控制介面',
                        text=f"裝置狀態: {'開' if ac_on is True else '關'} / 設定: {ac_set_temp}°C / 環境: {ac_ambient_temp}°C",
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
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/af_white.jpg',
                        image_aspect_ratio='rectangle',
                        image_size='contain',
                        title='空氣清淨機控制介面',
                        text=f"裝置狀態: {'開' if af_on is True else '關'} / PM2.5: {af_pm25}",
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
            elif text == "啟動回家模式":
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text="回家模式已啟動")]
                )
            elif text == "回家模式":
                flex_contents = get_flex("go_home")
                line_bot_api.reply_message(
                    event.reply_token, [FlexSendMessage(alt_text="(設定介面)", contents=flex_contents)]
                )
            elif text == "出門模式":
                flex_contents = get_flex("go_out")
                line_bot_api.reply_message(
                    event.reply_token, [FlexSendMessage(alt_text="(設定介面)", contents=flex_contents)]
                )
            elif text == "全家出門模式":
                flex_contents = get_flex("all_go_out")
                line_bot_api.reply_message(
                    event.reply_token, [FlexSendMessage(alt_text="(設定介面)", contents=flex_contents)]
                )
            elif text == "晚安模式":  # FIXME: activate by request, not by button
                # TODO: request IoT to execute
                vacuum_on_off(event.reply_token)
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="關燈"),
                        TextSendMessage(text="關窗簾"),
                        TextSendMessage(text="打開清淨機"),
                        TextSendMessage(text="掃地機回家")
                    ]
                )
            elif text == "早安模式":  # FIXME: activate by request, not by button
                # TODO: request IoT to execute
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="開燈"),
                        TextSendMessage(text="開窗簾"),
                        TextSendMessage(text="關閉清淨機")
                    ]
                )
            elif text == "午安模式":  # FIXME: activate by request, not by button
                # TODO: request IoT to execute
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="關窗簾"),
                        TextSendMessage(text="開冷氣")
                    ]
                )
            elif "資訊" in text:
                info_contents = get_info(text.replace("資訊", ''))
                line_bot_api.reply_message(
                    event.reply_token, [FlexSendMessage(alt_text="(資訊總覽)", contents=info_contents)]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text="無此功能")]
                )
        elif isinstance(event, PostbackEvent):  # postback event
            data = event.postback.data
            # TODO: resend updated state as text or small flex
            # on/off control
            if data == "fan_onoff":
                fan_on_off(event.reply_token)
            elif data == "vacuum_onoff":
                vacuum_on_off(event.reply_token)
            elif data == "ac_onoff":
                ac_on_off(event.reply_token)
            elif data == "af_onoff":
                af_on_off(event.reply_token)
            
            # fan speed control and turn toggle
            elif data == "fan_speed_up":
                fan_control_speed_up(event.reply_token)
            elif data == "fan_speed_down":
                fan_control_speed_down(event.reply_token)
            elif data == "fan_turn_toggle":
                fan_control_turn_toggle(event.reply_token)
            
            # ac setting temperature control
            elif data == "ac_temp_up" or data == "ac_temp_down":
                ac_control_set_temp(data.split('_')[-1], event.reply_token)
            
            # delete boxe in scenario
            elif "remove_" in data:
                remove_box(data, event.reply_token)
            
            # add boxes in scenario
            elif "add_" in data:
                add_box_reply(data, event.reply_token)
            elif "insert_" in data:
                add_box_execute(data, event.reply_token)
            
            # adjust ac temp or fan speed, turn in scenario
            elif "adjust_" in data:
                adjust_box(data, event.reply_token)
            
            # richmenu switch
            elif "richmenu-changed-to-" in data:
                global current_tab
                current_tab = str(data).strip().split('-')[-1]
                print(f"Richmenu switched: {current_tab=}")
            else:
                line_bot_api.reply_message(
                    event.reply_token, [TextSendMessage(text="無此功能")]
                )
        
        update_database()  # write updated global variables states back to MongoDB
        
        
    return 'OK'


def update_devices_state():
    global fan_on, fan_speed, fan_turn, ac_on, ac_set_temp, ac_ambient_temp, af_on, af_pm25, vacuum_on#, boxes
    body = {
        "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
        "inputs": [{
            "intent": "action.devices.QUERY",
            "payload": {
                "devices": [
                    {"id": ac_id},  # A/C
                    {"id": af_id},  # A/F
                    {"id": fan_id},   # fan
                    {"id": vacuum_id}   # vacuum
                ]
            }
        }]
    }
    r = requests.post(url, data=json.dumps(body), headers=headers)
    r_dict = r.json()
    print(r_dict)
    for device in r_dict["payload"]["devices"]:
        #FIXME: can't update vacuum state yet
        if fan_id in device.keys() and device[fan_id]["online"] == True:
            fan_on = bool(device[fan_id]["on"])
            fan_speed = int(device[fan_id]["currentFanSpeedSetting"])
            fan_turn = bool(device[fan_id]["currentToggleSettings"]["turn_toggle"])
            print(f"Update fan: {fan_on=}, {fan_speed=}, {fan_turn=}")
        elif ac_id in device.keys() and device[ac_id]["online"] == True:
            ac_on = bool(device[ac_id]["on"])
            ac_set_temp = int(device[ac_id]["thermostatTemperatureSetpoint"])
            ac_ambient_temp = int(device[ac_id]["thermostatTemperatureAmbient"])
            print(f"Update ac: {ac_on=}, {ac_set_temp=}, {ac_ambient_temp=}")
        elif af_id in device.keys() and device[af_id]["online"] == True:
            af_on = bool(device[af_id]["on"])
            af_pm25 = float(device[af_id]["currentSensorStateData"][0]["rawValue"])  #FIXME: float or int ?
            print(f"Update af: {af_on=}, {af_pm25=}")
        elif vacuum_id in device.keys() and device[vacuum_id]["online"] == True:
            vacuum_on = bool(device[vacuum_id]["isRunning"])
            print(f"Update vacuum: {vacuum_on=}")
        else:
            print(f"Unknown device: {device.keys()}")
    # boxes["ac_box"]["contents"][1]["text"] = f"{'on' if ac_on is True else 'off'} / {ac_set_temp}°C"
    # boxes["fan_box"]["contents"][1]["text"] = f"{'on' if fan_on is True else 'off'} / 風速 {fan_speed} / {'擺頭' if fan_turn is True else '固定'}"
    # boxes["af_box"]["contents"][1]["text"] = f"{'on' if af_on is True else 'off'} / {int(af_pm25)} PM2.5"
    # boxes["vacuum_box"]["contents"][1]["text"] = f"{'on / 清掃中' if vacuum_on is True else 'off / 充電中'}"


def load_database():
    # global fan_on, fan_speed, fan_turn, ac_on, ac_set_temp, ac_ambient_temp, af_on, af_pm25, vacuum_on, current_tab, scenarios_on_off
    result = states.find_one(object_id_dict)
    for key, value in result.items():
        if key != "_id":
            globals()[key] = value


def update_database():
    states.replace_one(object_id_dict, get_state0())


def fan_on_off(reply_token):
    with open("static/body_onoff.json", encoding="utf-8") as f:
        body = json.load(f)
    body["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"] = fan_id
    if fan_on is True:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["on"] = False
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="電扇已關閉")
        )
    elif fan_on is False:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["on"] = True
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="電扇已開啟")
        )
    else:
        print(f"ERROR: wrong fan_on value = {fan_on}")


def ac_on_off(reply_token):
    with open("static/body_onoff.json", encoding="utf-8") as f:
            body = json.load(f)
    body["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"] = ac_id
    if ac_on is True:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["on"] = False
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="冷氣已關閉")
        )
    elif ac_on is False:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["on"] = True
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="冷氣已開啟")
        )
    else:
        print(f"ERROR: wrong ac_on value = {ac_on}")


def af_on_off(reply_token):
    with open("static/body_onoff.json", encoding="utf-8") as f:
            body = json.load(f)
    body["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"] = af_id
    if af_on is True:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["on"] = False
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="空氣清淨機已關閉")
        )
    elif af_on is False:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["on"] = True
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="空氣清淨機已開啟")
        )
    else:
        print(f"ERROR: wrong af_on value = {af_on}")


def vacuum_on_off(reply_token):
    with open("static/body_onoff.json", encoding="utf-8") as f:
            body = json.load(f)
    body["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"] = vacuum_id
    if vacuum_on is True:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["command"] = "action.devices.commands.Dock"
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"] = {}
        r = requests.post(url, data=json.dumps(body), headers=headers)
        # r_dict = json.loads(r.text.replace("123", ''))
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="掃地機已回家")
        )
    elif vacuum_on is False:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["command"] = "action.devices.commands.StartStop"
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"] = {"start": True}
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = json.loads(r.text.replace("123", ''))
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="掃地機開始打掃")
        )
    else:
        print(f"ERROR: wrong vacuum_on value = {vacuum_on}")


def get_flex(scenario):
    with open(f"static/flex_scenario_all.json", encoding="utf-8") as f:
        flex_dict = json.load(f)
    boxes = get_boxes(scenario)
    if scenario == "go_out":
        flex_dict["header"]["contents"][0]["text"] = "出門模式設定介面"
    elif scenario == "all_go_out":
        flex_dict["header"]["contents"][0]["text"] = "全家出門模式介面"
    elif scenario == "go_home":
        flex_dict["header"]["contents"][0]["text"] = "回家模式設定介面"
    else:
        print(f"Wrong value: {scenario=}")
        
    flex_dict["body"]["contents"][0]["contents"][0]["contents"] = [boxes[box] for box in scenarios_on_off[f"{scenario}_on"]]
    flex_dict["body"]["contents"][0]["contents"][2]["contents"] = [boxes[box] for box in scenarios_on_off[f"{scenario}_off"]]
    return flex_dict


def get_info(room):
    with open(f"static/info.json", encoding="utf-8") as f:
        info_dict = json.load(f)
    if room == "客廳":
        info_dict["body"]["contents"][0]["url"] = f"https://serene-stream-27454.herokuapp.com/static/livingRoom.jpg"
    elif room == "主臥":
        info_dict["body"]["contents"][0]["url"] = f"https://serene-stream-27454.herokuapp.com/static/masterBedroom.jpg"
    elif room == "長輩房":
        info_dict["body"]["contents"][0]["url"] = f"https://serene-stream-27454.herokuapp.com/static/elderBedroom.jpg"
    else:
        pass
    print(f'{room}: info_dict["body"]["contents"][0]["url"]')
    info_dict["body"]["contents"][2]["contents"][0]["contents"][1]["contents"][1]["text"] = f"裝置狀態: {'開' if fan_on else '關'}"
    info_dict["body"]["contents"][2]["contents"][2]["contents"][1]["contents"][1]["text"] = f"裝置狀態: {'開' if ac_on else '關'}"
    info_dict["body"]["contents"][4]["contents"][0]["contents"][1]["contents"][1]["text"] = f"裝置狀態: {'開' if af_on else '關'}"
    info_dict["body"]["contents"][4]["contents"][2]["contents"][1]["contents"][1]["text"] = f"裝置狀態: {'開' if vacuum_on else '關'}"
    
    info_dict["body"]["contents"][2]["contents"][0]["contents"][1]["contents"][2]["text"] = f"風速: {fan_speed}"
    info_dict["body"]["contents"][2]["contents"][0]["contents"][1]["contents"][3]["text"] = f"風向: {'擺頭' if fan_turn else '固定'}"
    info_dict["body"]["contents"][2]["contents"][2]["contents"][1]["contents"][2]["text"] = f"環境: {ac_ambient_temp}°C"
    info_dict["body"]["contents"][2]["contents"][2]["contents"][1]["contents"][3]["text"] = f"設定: {ac_set_temp}°C"
    info_dict["body"]["contents"][4]["contents"][0]["contents"][1]["contents"][2]["text"] = f"PM2.5: {af_pm25}"
    info_dict["body"]["contents"][4]["contents"][2]["contents"][1]["contents"][2]["text"] = f"{'掃地中' if vacuum_on else '充電中'}"
    return info_dict


def fan_control_speed_up(reply_token):
    with open("static/body_SetFanSpeed.json", encoding="utf-8") as f:
        body = json.load(f)
    body["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"] = fan_id
    body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["fanSpeed"] = "speed_up"
    r = requests.post(url, data=json.dumps(body), headers=headers)
    r_dict = r.json()
    print(r_dict)
    # update_devices_state()  # FIXME: query update too fast, fan speed control not yet executed
    line_bot_api.reply_message(
        reply_token, TextSendMessage(text=f"已增強電扇風量")#為: {fan_speed}")
    )


def fan_control_speed_down(reply_token):
    with open("static/body_SetFanSpeed.json", encoding="utf-8") as f:
        body = json.load(f)
    body["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"] = fan_id
    body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["fanSpeed"] = "speed_dow"
    r = requests.post(url, data=json.dumps(body), headers=headers)
    r_dict = r.json()
    print(r_dict)
    # update_devices_state()  # FIXME: query update too fast, fan speed control not yet executed
    line_bot_api.reply_message(
        reply_token, TextSendMessage(text=f"已降低電扇風量")#為: {fan_speed}")
    )


def fan_control_turn_toggle(reply_token):
    with open("static/body_SetToggles.json", encoding="utf-8") as f:
        body = json.load(f)
    body["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"] = fan_id
    if fan_turn is True:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["updateToggleSettings"]["turn_toggle"] = False
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"風扇風向已固定")
        )
    elif fan_turn is False:
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["updateToggleSettings"]["turn_toggle"] = True
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"風扇風向已擺頭")
        )
    else:
        print(f"ERROR: wrong value: {fan_turn=}")


def ac_control_set_temp(down_or_up, reply_token):
    with open("static/body_SetACTemp.json", encoding="utf-8") as f:
        body = json.load(f)
    body["inputs"][0]["payload"]["commands"][0]["devices"][0]["id"] = ac_id
    if down_or_up == "up":
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["thermostatTemperatureSetpoint"] = ac_set_temp + 1
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"已調高冷氣溫度")
        )
    elif down_or_up == "down":
        body["inputs"][0]["payload"]["commands"][0]["execution"][0]["params"]["thermostatTemperatureSetpoint"] = ac_set_temp - 1
        r = requests.post(url, data=json.dumps(body), headers=headers)
        r_dict = r.json()
        print(r_dict)
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"已調低冷氣溫度")
        )
    else:
        print(f"ERROR: wrong value: {down_or_up=}")


def remove_box(data, reply_token):
    global scenarios_on_off
    box_name = data.split('_')[1] + "_box"  # >>> "ac_box"
    scenario_name = data.replace(f"remove_{data.split('_')[1]}_", '')  # >>> "go_home" or ...
    scenarios_on_off[scenario_name + "_on"] = [box for box in scenarios_on_off[scenario_name + "_on"] if box != box_name]
    scenarios_on_off[scenario_name + "_off"] = [box for box in scenarios_on_off[scenario_name + "_off"] if box != box_name]
    flex_contents = get_flex(scenario_name)
    line_bot_api.reply_message(
        reply_token, 
        [
            TextSendMessage(text="已刪除"),
            FlexSendMessage(alt_text="(設定介面)", contents=flex_contents)
        ]
    )


def add_box_reply(data, reply_token):
    global scenarios_on_off
    column_name = data.split('_')[1]  # >>> "on" or "off"
    scenario_name = data.replace(f"add_{column_name}_", '')  # >>> "go_home" or ...
    line_bot_api.reply_message(
        reply_token,
        [
            TextSendMessage(
                text="請選擇欲新增的家電",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            image_url=f"https://serene-stream-27454.herokuapp.com/static/{box.split('_')[-1]}_white.jpg",
                            action=PostbackAction(label=box.split('_')[0], data=f"insert_{column_name}_{box.split('_')[-1]}_{scenario_name}")
                        )
                        for box in ["電扇_fan", "冷氣_ac", "清淨機_af", "掃地機_vacuum"]
                        if box.split('_')[-1]+"_box" not in scenarios_on_off[f"{scenario_name}_on"] + scenarios_on_off[f"{scenario_name}_off"]
                    ] + [QuickReplyButton(action=PostbackAction(label="取消", data="insert_cancel"))]
                )
            )
        ]
    )


def add_box_execute(data, reply_token):
    global scenarios_on_off
    if "cancel" not in data:
        column_name = data.split('_')[1]  # >>> "on" or "off"
        device_name = data.split('_')[2]  # >>> "fan" or ...
        scenario_name = data.replace(f"insert_{column_name}_{device_name}_", '')  # >>> "go_home" or ...
        scenarios_on_off[f"{scenario_name}_{column_name}"].insert(-1, f"{device_name}_box")
        flex_contents = get_flex(scenario_name)
        line_bot_api.reply_message(
            reply_token,
            [
                TextSendMessage(text="已新增家電至情境"),
                FlexSendMessage(alt_text="(設定介面)", contents=flex_contents)
            ]
        )
    elif "cancel" in data:
        line_bot_api.reply_message(
            reply_token, [TextSendMessage(text="已取消新增")]
        )
    else:
        line_bot_api.reply_message(
            reply_token, [TextSendMessage(text="無此功能")]
        )


def adjust_box(data, reply_token):  # data = "adjust_speed", "a"
    task = data.split('_')[1]  # >>> "fan", "ac", "speedUp", "speedDown", "turn", "fixed", "tempUp", "tempDown"
    scenario_name = data.replace(f"adjust_{task}_", '')
    global scenarios_settings
    if task == "fan":
        line_bot_api.reply_message(
            reply_token,
            [
                TextSendMessage(
                    text="請選擇欲調整的設定",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=PostbackAction(label="增強風量", data=f"adjust_speedUp_{scenario_name}")),
                            QuickReplyButton(action=PostbackAction(label="降低風量", data=f"adjust_speedDown_{scenario_name}")),
                            QuickReplyButton(action=PostbackAction(label="風向固定", data=f"adjust_turn_{scenario_name}")),
                            QuickReplyButton(action=PostbackAction(label="風向擺頭", data=f"adjust_fixed_{scenario_name}"))
                        ]
                    )
                )
            ]
        )
    elif task == "ac":
        line_bot_api.reply_message(
            reply_token,
            [
                TextSendMessage(
                    text="請選擇欲調整的設定",
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=PostbackAction(label="溫度升", data=f"adjust_tempUp_{scenario_name}")),
                            QuickReplyButton(action=PostbackAction(label="溫度降", data=f"adjust_tempDown_{scenario_name}"))
                        ]
                    )
                )
            ]
        )
    elif task == "speedUp":
        scenarios_settings[scenario_name]["speed"] += 1  #FIXME: clamp the value range
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"已設定該模式風速為{scenarios_settings[scenario_name]['speed']}")
        )
    elif task == "speedDown":
        scenarios_settings[scenario_name]["speed"] -= 1  #FIXME: clamp the value range
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"已設定該模式風速為{scenarios_settings[scenario_name]['speed']}")
        )
    elif task == "turn":
        scenarios_settings[scenario_name]["turn"] = True
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"已設定該模式風向為擺頭")
        )
    elif task == "fixed":
        scenarios_settings[scenario_name]["turn"] = False
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"已設定該模式風向為固定")
        )
    elif task == "tempUp":
        scenarios_settings[scenario_name]["temp"] += 1  #FIXME: clamp the value range
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"已設定該模式溫度為{scenarios_settings[scenario_name]['temp']}")
        )
    elif task == "tempDown":
        scenarios_settings[scenario_name]["temp"] -= 1  #FIXME: clamp the value range
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text=f"已設定該模式溫度為{scenarios_settings[scenario_name]['temp']}")
        )
    else:
        line_bot_api.reply_message(
            reply_token, TextSendMessage(text="無此功能")
        )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
