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

# State of the devices
# - Fan
fan_on = None  # True, False
fan_speed = None  # int
# - A/C
ac_on = None  # True, False
ac_set_temp = None  # int
ac_ambient_temp = None  # int 
# - A/F
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
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):  # text message
            text = event.message.text
            if text == "哈囉":
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
            elif text == "電風扇控制":
                update_devces_state()
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
                                label='postback',
                                display_text='postback text',
                                data='action=buy&itemid=1'
                            ),
                            MessageAction(
                                label='message',
                                text='message text'
                            ),
                            URIAction(
                                label='uri',
                                uri='http://www.google.com/'
                            )
                        ]
                    )
                )
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
                                label='postback',
                                display_text='postback text',
                                data='action=buy&itemid=1'
                            ),
                            MessageAction(
                                label='message',
                                text='message text'
                            ),
                            URIAction(
                                label='uri',
                                uri='http://www.google.com/'
                            )
                        ]
                    )
                )
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
                                label='postback',
                                display_text='postback text',
                                data='action=buy&itemid=1'
                            ),
                            MessageAction(
                                label='message',
                                text='message text'
                            ),
                            URIAction(
                                label='uri',
                                uri='http://www.google.com/'
                            )
                        ]
                    )
                )
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
                                label='postback',
                                display_text='postback text',
                                data='action=buy&itemid=1'
                            ),
                            MessageAction(
                                label='message',
                                text='message text'
                            ),
                            URIAction(
                                label='uri',
                                uri='http://www.google.com/'
                            )
                        ]
                    )
                )
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        buttons_message_fan,
                        buttons_message_vacuum,
                        buttons_message_ac,
                        buttons_message_af
                    ]
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        TextSendMessage(text="Wrong keywords"),
                    ]
                )

    return 'OK'


def update_devces_state():
    access_token = os.getenv('access_token', None)
    url = "https://iot.jowinwin.com/iot_tds/control.php"
    body = {
        "requestId": "ff36a3cc-ec34-11e6-b1a0-64510650abcf",
        "inputs": [{
            "intent": "action.devices.QUERY",
            "payload": {
                "devices": [
                    {"id": "a00abf1dd7e7"},  # A/C
                    {"id": "a00abf1ddb09"},  # A/F
                    {"id": "a00abf394b1c"}   # fan
                ]
            }
        }]
    }
    headers = {"Authorization": "Bearer " + access_token}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    r_json = r.json()
    print(r_json)
    



if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
