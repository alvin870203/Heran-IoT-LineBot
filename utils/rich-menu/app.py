# -*- coding: utf-8 -*-

import os
import sys

from linebot import (
    LineBotApi,
)

from linebot.models import (
    RichMenu,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    URIAction
)
from linebot.models.actions import MessageAction, RichMenuSwitchAction
from linebot.models.rich_menu import RichMenuAlias

# FIXME: use environment variable to store channel access token in production for security safety
# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_access_token = "kv7jk24WGVyrxdaWgHp0fEZnyuql5FUM6TdppyQrehca1ACgXGIgfrxXfeMnG44jlwoJOjZ8czICeCvBCCLIq0sScVGF1TAqqfvcSa9bVHJOcPR3SrXq2tq57PVYdYByQuPATvWve8bnJ1S1oEA5FQdB04t89/1O/w1cDnyilFU="

if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)


def rich_menu_object_scenario_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "richmenu-scenario",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 641,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-scenario",
                    "data": "richmenu-changed-to-scenario"
                }
            },
            {
                "bounds": {
                    "x": 641,
                    "y": 0,
                    "width": 621,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-living_room",
                    "data": "richmenu-changed-to-living_room"
                }
            },
            {
                "bounds": {
                    "x": 1268,
                    "y": 0,
                    "width": 627,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-master_bedroom",
                    "data": "richmenu-changed-to-master_bedroom"
                }
            },
            {
                "bounds": {
                    "x": 1890,
                    "y": 0,
                    "width": 609,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-elder_bedroom",
                    "data": "richmenu-changed-to-elder_bedroom"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 188,
                    "width": 831,
                    "height": 744
                },
                "action": {
                    "type": "message",
                    "text": "出門模式"
                }
            },
            {
                "bounds": {
                    "x": 831,
                    "y": 190,
                    "width": 834,
                    "height": 742
                },
                "action": {
                    "type": "message",
                    "text": "回家模式"
                }
            },
            {
                "bounds": {
                    "x": 1671,
                    "y": 190,
                    "width": 820,
                    "height": 739
                },
                "action": {
                    "type": "message",
                    "text": "全家出門模式"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 940,
                    "width": 827,
                    "height": 746
                },
                "action": {
                    "type": "message",
                    "text": "早安模式"
                }
            },
            {
                "bounds": {
                    "x": 833,
                    "y": 940,
                    "width": 832,
                    "height": 746
                },
                "action": {
                    "type": "message",
                    "text": "午安模式"
                }
            },
            {
                "bounds": {
                    "x": 1673,
                    "y": 942,
                    "width": 812,
                    "height": 744
                },
                "action": {
                    "type": "message",
                    "text": "晚安模式"
                }
            }
        ]
    }

def rich_menu_object_living_room_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "richmenu-living_room",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 641,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-scenario",
                    "data": "richmenu-changed-to-scenario"
                }
            },
            {
                "bounds": {
                    "x": 641,
                    "y": 0,
                    "width": 621,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-living_room",
                    "data": "richmenu-changed-to-living_room"
                }
            },
            {
                "bounds": {
                    "x": 1268,
                    "y": 0,
                    "width": 627,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-master_bedroom",
                    "data": "richmenu-changed-to-master_bedroom"
                }
            },
            {
                "bounds": {
                    "x": 1890,
                    "y": 0,
                    "width": 609,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-elder_bedroom",
                    "data": "richmenu-changed-to-elder_bedroom"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 188,
                    "width": 831,
                    "height": 744
                },
                "action": {
                    "type": "message",
                    "text": "客廳資訊"
                }
            },
            {
                "bounds": {
                    "x": 831,
                    "y": 190,
                    "width": 834,
                    "height": 742
                },
                "action": {
                    "type": "message",
                    "text": "電風扇"
                }
            },
            {
                "bounds": {
                    "x": 1671,
                    "y": 190,
                    "width": 820,
                    "height": 739
                },
                "action": {
                    "type": "message",
                    "text": "掃地機"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 940,
                    "width": 827,
                    "height": 746
                },
                "action": {
                    "type": "message",
                    "text": "除濕機"
                }
            },
            {
                "bounds": {
                    "x": 833,
                    "y": 940,
                    "width": 832,
                    "height": 746
                },
                "action": {
                    "type": "message",
                    "text": "空氣清淨機"
                }
            },
            {
                "bounds": {
                    "x": 1673,
                    "y": 942,
                    "width": 812,
                    "height": 744
                },
                "action": {
                    "type": "message",
                    "text": "冷氣"
                }
            }
        ]
    }

def rich_menu_object_master_bedroom_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "richmenu-master_bedroom",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 641,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-scenario",
                    "data": "richmenu-changed-to-scenario"
                }
            },
            {
                "bounds": {
                    "x": 641,
                    "y": 0,
                    "width": 621,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-living_room",
                    "data": "richmenu-changed-to-living_room"
                }
            },
            {
                "bounds": {
                    "x": 1268,
                    "y": 0,
                    "width": 627,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-master_bedroom",
                    "data": "richmenu-changed-to-master_bedroom"
                }
            },
            {
                "bounds": {
                    "x": 1890,
                    "y": 0,
                    "width": 609,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-elder_bedroom",
                    "data": "richmenu-changed-to-elder_bedroom"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 188,
                    "width": 831,
                    "height": 744
                },
                "action": {
                    "type": "message",
                    "text": "主臥資訊"
                }
            },
            {
                "bounds": {
                    "x": 831,
                    "y": 190,
                    "width": 834,
                    "height": 742
                },
                "action": {
                    "type": "message",
                    "text": "電風扇"
                }
            },
            {
                "bounds": {
                    "x": 1671,
                    "y": 190,
                    "width": 820,
                    "height": 739
                },
                "action": {
                    "type": "message",
                    "text": "掃地機"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 940,
                    "width": 827,
                    "height": 746
                },
                "action": {
                    "type": "message",
                    "text": "除濕機"
                }
            },
            {
                "bounds": {
                    "x": 833,
                    "y": 940,
                    "width": 832,
                    "height": 746
                },
                "action": {
                    "type": "message",
                    "text": "空氣清淨機"
                }
            },
            {
                "bounds": {
                    "x": 1673,
                    "y": 942,
                    "width": 812,
                    "height": 744
                },
                "action": {
                    "type": "message",
                    "text": "冷氣"
                }
            }
        ]
    }

def rich_menu_object_elder_bedroom_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "richmenu-elder_bedroom",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 641,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-scenario",
                    "data": "richmenu-changed-to-scenario"
                }
            },
            {
                "bounds": {
                    "x": 641,
                    "y": 0,
                    "width": 621,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-living_room",
                    "data": "richmenu-changed-to-living_room"
                }
            },
            {
                "bounds": {
                    "x": 1268,
                    "y": 0,
                    "width": 627,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-master_bedroom",
                    "data": "richmenu-changed-to-master_bedroom"
                }
            },
            {
                "bounds": {
                    "x": 1890,
                    "y": 0,
                    "width": 609,
                    "height": 184
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-elder_bedroom",
                    "data": "richmenu-changed-to-elder_bedroom"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 188,
                    "width": 831,
                    "height": 744
                },
                "action": {
                    "type": "message",
                    "text": "長輩房資訊"
                }
            },
            {
                "bounds": {
                    "x": 831,
                    "y": 190,
                    "width": 834,
                    "height": 742
                },
                "action": {
                    "type": "message",
                    "text": "電風扇"
                }
            },
            {
                "bounds": {
                    "x": 1671,
                    "y": 190,
                    "width": 820,
                    "height": 739
                },
                "action": {
                    "type": "message",
                    "text": "掃地機"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 940,
                    "width": 827,
                    "height": 746
                },
                "action": {
                    "type": "message",
                    "text": "除濕機"
                }
            },
            {
                "bounds": {
                    "x": 833,
                    "y": 940,
                    "width": 832,
                    "height": 746
                },
                "action": {
                    "type": "message",
                    "text": "空氣清淨機"
                }
            },
            {
                "bounds": {
                    "x": 1673,
                    "y": 942,
                    "width": 812,
                    "height": 744
                },
                "action": {
                    "type": "message",
                    "text": "冷氣"
                }
            }
        ]
    }


# def rich_menu_object_b_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "richmenu-b",
        "chatBarText": "Tap to open",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 1250,
                    "height": 1686
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-scenario",
                    "data": "richmenu-changed-to-scenario"
                }
            },
            {
                "bounds": {
                    "x": 1251,
                    "y": 0,
                    "width": 1250,
                    "height": 1686
                },
                "action": {
                    "type": "uri",
                    "uri": "https://www.line-community.me/"
                }
            }
        ]
    }


def create_action(action):
    if action['type'] == 'uri':
        return URIAction(type=action['type'], uri=action.get('uri'))
    elif action['type'] == 'message':
        return MessageAction(type=action['type'], text=action.get('text'))
    else:
        return RichMenuSwitchAction(
            type=action['type'],
            rich_menu_alias_id=action.get('richMenuAliasId'),
            data=action.get('data')
        )


def main():
    # 2. Create rich menu Scenario (richmenu-scenario)
    rich_menu_object_scenario = rich_menu_object_scenario_json()
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=info['bounds']['x'],
                y=info['bounds']['y'],
                width=info['bounds']['width'],
                height=info['bounds']['height']
            ),
            action=create_action(info['action'])
        ) for info in rich_menu_object_scenario['areas']
    ]

    rich_menu_to_scenario_create = RichMenu(
        size=RichMenuSize(width=rich_menu_object_scenario['size']['width'], height=rich_menu_object_scenario['size']['height']),
        selected=rich_menu_object_scenario['selected'],
        name=rich_menu_object_scenario['name'],
        chat_bar_text=rich_menu_object_scenario['chatBarText'],
        areas=areas
    )

    rich_menu_scenario_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_scenario_create)

    # 2. Create rich menu Living Room (richmenu-living_room)
    rich_menu_object_living_room = rich_menu_object_living_room_json()
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=info['bounds']['x'],
                y=info['bounds']['y'],
                width=info['bounds']['width'],
                height=info['bounds']['height']
            ),
            action=create_action(info['action'])
        ) for info in rich_menu_object_living_room['areas']
    ]

    rich_menu_to_living_room_create = RichMenu(
        size=RichMenuSize(width=rich_menu_object_living_room['size']['width'], height=rich_menu_object_living_room['size']['height']),
        selected=rich_menu_object_living_room['selected'],
        name=rich_menu_object_living_room['name'],
        chat_bar_text=rich_menu_object_living_room['chatBarText'],
        areas=areas
    )

    rich_menu_living_room_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_living_room_create)

    # 2. Create rich menu Master Bedroom (richmenu-master_bedroom)
    rich_menu_object_master_bedroom = rich_menu_object_master_bedroom_json()
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=info['bounds']['x'],
                y=info['bounds']['y'],
                width=info['bounds']['width'],
                height=info['bounds']['height']
            ),
            action=create_action(info['action'])
        ) for info in rich_menu_object_master_bedroom['areas']
    ]

    rich_menu_to_master_bedroom_create = RichMenu(
        size=RichMenuSize(width=rich_menu_object_master_bedroom['size']['width'], height=rich_menu_object_master_bedroom['size']['height']),
        selected=rich_menu_object_master_bedroom['selected'],
        name=rich_menu_object_master_bedroom['name'],
        chat_bar_text=rich_menu_object_master_bedroom['chatBarText'],
        areas=areas
    )

    rich_menu_master_bedroom_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_master_bedroom_create)

    # 2. Create rich menu Elder Bedroom (richmenu-elder_bedroom)
    rich_menu_object_elder_bedroom = rich_menu_object_elder_bedroom_json()
    areas = [
        RichMenuArea(
            bounds=RichMenuBounds(
                x=info['bounds']['x'],
                y=info['bounds']['y'],
                width=info['bounds']['width'],
                height=info['bounds']['height']
            ),
            action=create_action(info['action'])
        ) for info in rich_menu_object_elder_bedroom['areas']
    ]

    rich_menu_to_elder_bedroom_create = RichMenu(
        size=RichMenuSize(width=rich_menu_object_elder_bedroom['size']['width'], height=rich_menu_object_elder_bedroom['size']['height']),
        selected=rich_menu_object_elder_bedroom['selected'],
        name=rich_menu_object_elder_bedroom['name'],
        chat_bar_text=rich_menu_object_elder_bedroom['chatBarText'],
        areas=areas
    )

    rich_menu_elder_bedroom_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_elder_bedroom_create)


    # 3. Upload image to rich menu Scenario
    with open('../richmenu_figs/scenario/情境模式_tab2.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_scenario_id, 'image/png', f)

    # 3. Upload image to rich menu Living Room
    with open('../richmenu_figs/living_room/客廳_tab2.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_living_room_id, 'image/png', f)

    # 3. Upload image to rich menu Master Bedroom
    with open('../richmenu_figs/master_bedroom/主臥_tab2.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_master_bedroom_id, 'image/png', f)

    # 3. Upload image to rich menu Elder Bedroom
    with open('../richmenu_figs/elder_bedroom/長輩房_tab2.png', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_elder_bedroom_id, 'image/png', f)


    # 6. Set rich menu Scenario as the default rich menu
    line_bot_api.set_default_rich_menu(rich_menu_scenario_id)


    # 7. Create rich menu alias Scenario
    alias_scenario = RichMenuAlias(
        rich_menu_alias_id='richmenu-alias-scenario',
        rich_menu_id=rich_menu_scenario_id
    )
    line_bot_api.create_rich_menu_alias(alias_scenario)

    # 7. Create rich menu alias Living Room
    alias_living_room = RichMenuAlias(
        rich_menu_alias_id='richmenu-alias-living_room',
        rich_menu_id=rich_menu_living_room_id
    )
    line_bot_api.create_rich_menu_alias(alias_living_room)

    # 7. Create rich menu alias Master Bedroom
    alias_master_bedroom = RichMenuAlias(
        rich_menu_alias_id='richmenu-alias-master_bedroom',
        rich_menu_id=rich_menu_master_bedroom_id
    )
    line_bot_api.create_rich_menu_alias(alias_master_bedroom)

    # 7. Create rich menu alias Elder Bedroom
    alias_elder_bedroom = RichMenuAlias(
        rich_menu_alias_id='richmenu-alias-elder_bedroom',
        rich_menu_id=rich_menu_elder_bedroom_id
    )
    line_bot_api.create_rich_menu_alias(alias_elder_bedroom)


    print('success')


main()


# Delete all rich menu automatically
def delete_and_check_rich_menu():
    import json
    # line_bot_api.delete_rich_menu("richmenu-8ac3456b8d9b145418bce78027cd650e")
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        # print(json.dumps(json.loads(str(rich_menu)), indent=4, sort_keys=True))
        rich_menu_id = json.loads(str(rich_menu)).get("richMenuId")
        print(rich_menu_id)
        # line_bot_api.delete_rich_menu(rich_menu_id)
    print(len(rich_menu_list))
    
# delete_and_check_rich_menu()