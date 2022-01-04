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
                buttons_message_fan = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/電風扇.jpg',
                        image_aspect_ratio='square',
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
                buttons_message_vaccum = TemplateSendMessage(
                    alt_text='Buttons template',
                    template=ButtonsTemplate(
                        thumbnail_image_url='https:/serene-stream-27454.herokuapp.com/static/掃地機.jpg',
                        image_aspect_ratio='square',
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
                        image_aspect_ratio='square',
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
                        image_aspect_ratio='square',
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
                        buttons_message_vaccum,
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


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
