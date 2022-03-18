import datetime
import json
import random
import secrets
import string
import uuid
import time

import requests
from pypika import PostgreSQLQuery, Table

import database
import device_util as du


# region Report Device Info
def report_device_info(device_name, device_uid, device_os, device_gpu, device_cpu, session_ticket):
    url = 'https://2ffe4.playfabapi.com/Client/ReportDeviceInfo'
    data = {
        "Info": {
            "ProductName": "Electus Online",
            "ProductBundle": "com.Electus.ElectusOnline",
            "Version": "0.31",
            "Company": "Electus",
            "Platform": "Android",
            "GraphicsMultiThreaded": True,
            "GraphicsType": "OpenGLES3",
            "DataPath": "/data/app/com.Electus.ElectusOnline/base.apk",
            "PersistentDataPath": "/storage/emulated/0/Android/data/com.Electus.ElectusOnline/files",
            "StreamingAssetsPath": "jar:file:///data/app/com.Electus.ElectusOnline/base.apk!/assets",
            "TargetFrameRate": -1,
            "UnityVersion": "2020.1.10f1",
            "RunInBackground": True,
            "DeviceModel": device_name,
            "DeviceType": "Handheld",
            "DeviceUniqueId": device_uid,
            "OperatingSystem": device_os,
            "GraphicsDeviceId": 0,
            "GraphicsDeviceName": device_gpu,
            "GraphicsMemorySize": random.randint(256, 1024),
            "GraphicsShaderLevel": 45,
            "SystemMemorySize": random.randint(2500, 8000),
            "ProcessorCount": 4,
            "ProcessorFrequency": random.randint(1500, 2500),
            "ProcessorType": device_cpu,
            "SupportsAccelerometer": True,
            "SupportsGyroscope": True,
            "SupportsLocationService": True
        },
        "AuthenticationContext": None
    }
    headers = {
        "x-authorization": session_ticket
    }
    return requests.post(url, json=data, headers=headers)


# endregion


# region Write Events
def write_events(entity_id, playfab_id, device_name, device_os, client_session_id, focus_id, entity_token):
    t = str(datetime.datetime.fromtimestamp(time.time()) - datetime.timedelta(random.randint(7, 25)))
    url = 'https://2ffe4.playfabapi.com/Event/WriteEvents'
    data = {
        "Events": [
            {
                "Entity": {
                    "Id": entity_id,
                    "Type": "title_player_account"
                },
                "EventNamespace": "com.playfab.events.sessions",
                "Name": "client_session_start",
                "OriginalId": None,
                "OriginalTimestamp": t,
                # "OriginalTimestamp": "2022-01-26T19:45:09.331Z",
                "Payload": {
                    "UserID": playfab_id,
                    "DeviceType": "Handheld",
                    "DeviceModel": device_name,
                    "OS": device_os,
                    "ClientSessionID": client_session_id
                },
                "PayloadJSON": None
            },
            {
                "Entity": {
                    "Id": entity_id,
                    "Type": "title_player_account"
                },
                "EventNamespace": "com.playfab.events.sessions",
                "Name": "client_focus_change",
                "OriginalId": None,
                "OriginalTimestamp": t,
                # "OriginalTimestamp": "2022-01-26T19:45:09.331Z",
                "Payload": {
                    "FocusID": focus_id,
                    "FocusState": True,
                    "FocusStateDuration": 0,
                    "EventTimestamp": t,
                    "ClientSessionID": client_session_id
                },
                "PayloadJSON": None
            }
        ],
        "AuthenticationContext": None
    }
    headers = {
        "x-entitytoken": entity_token
    }
    return requests.post(url, json=data, headers=headers)


# endregion


# region Android Device Push Notification Registration
def android_device_push_notification_registration(device_token, session_ticket):
    url = 'https://2ffe4.playfabapi.com/Client/AndroidDevicePushNotificationRegistration'
    data = {
        "ConfirmationMessage": "Push notifications registered successfully",
        "DeviceToken": device_token,
        "SendPushNotificationConfirmation": True,
        "AuthenticationContext": None
    }
    headers = {
        "x-authorization": session_ticket
    }
    return requests.post(url, json=data, headers=headers)


# endregion


# region Update User Data
def update_user_data(alchemy_time, session_ticket=None, android_id=None):
    if android_id is not None:
        login_account(android_id)
        accounts = Table('accounts')
        query = PostgreSQLQuery.from_(accounts).select("session_ticket").where(accounts.android_id == android_id)
        query = str(query)
        session_ticket = database.get_query(query)[0]
    url = 'https://2ffe4.playfabapi.com/Client/UpdateUserData'
    data = {
        "Data": {
            "AlchemyTime": alchemy_time
        },
        "KeysToRemove": None,
        "Permission": None,
        "AuthenticationContext": None
    }
    headers = {
        "x-authorization": session_ticket
    }
    return requests.post(url, json=data, headers=headers)


# endregion


# region Update User Title Display Name
def update_user_title_display_name(username, session_ticket=None, android_id=None):
    if android_id is not None:
        login_account(android_id)
        accounts = Table('accounts')
        query = PostgreSQLQuery.from_(accounts).select("session_ticket").where(accounts.android_id == android_id)
        query = str(query)
        session_ticket = database.get_query(query)[0]
    url = 'https://2ffe4.playfabapi.com/Client/UpdateUserTitleDisplayName'
    data = {
        "DisplayName": username,
        "AuthenticationContext": None
    }
    headers = {
        "x-authorization": session_ticket
    }
    return requests.post(url, json=data, headers=headers)


# endregion


# region Update Player Statistics
def update_player_statics(value, session_ticket=None, android_id=None):
    if android_id is not None:
        login_account(android_id)
        accounts = Table('accounts')
        query = PostgreSQLQuery.from_(accounts).select("session_ticket").where(accounts.android_id == android_id)
        query = str(query)
        session_ticket = database.get_query(query)[0]
    url = 'https://2ffe4.playfabapi.com/Client/UpdatePlayerStatistics'
    data = {
        "Statistics": [
            {
                "StatisticName": "ElectusPoints",
                "Value": value,
                "Version": None
            }
        ],
        "AuthenticationContext": None
    }
    headers = {
        "x-authorization": session_ticket
    }
    return requests.post(url, json=data, headers=headers)


# endregion


# region Update All Players Statistics
def update_all_players_statics(value):
    query = PostgreSQLQuery.from_('accounts').select('android_id')
    query = str(query)
    android_ids = database.get_query_all(query)
    android_ids = list(android_ids)
    for android_id in android_ids:
        android_id = android_id[0]
        login_account(android_id)
        accounts = Table('accounts')
        query = PostgreSQLQuery.from_(accounts).select("session_ticket").where(accounts.android_id == android_id)
        query = str(query)
        session_ticket = database.get_query(query)[0]
        url = 'https://2ffe4.playfabapi.com/Client/UpdatePlayerStatistics'
        data = {
            "Statistics": [
                {
                    "StatisticName": "ElectusPoints",
                    "Value": value,
                    "Version": None
                }
            ],
            "AuthenticationContext": None
        }
        headers = {
            "x-authorization": session_ticket
        }
        response = requests.post(url, json=data, headers=headers)
        print(android_id + "  ===>  " + str(response.status_code))


# endregion


# region Get User Data
def get_user_data(session_ticket=None, android_id=None):
    if android_id is not None:
        login_account(android_id)
        accounts = Table('accounts')
        query = PostgreSQLQuery.from_(accounts).select("session_ticket").where(accounts.android_id == android_id)
        query = str(query)
        session_ticket = database.get_query(query)[0]
    url = 'https://2ffe4.playfabapi.com/Client/GetUserData'
    data = {
        "IfChangedFromDataVersion": None,
        "Keys": [
            "AlchemyTime",
            "EP",
            "userName",
            "lastSilkGeneratorTime",
            "lastepin"
        ],
        "PlayFabId": None,
        "AuthenticationContext": None
    }
    headers = {
        "x-authorization": session_ticket
    }
    return requests.post(url, json=data, headers=headers)


# endregion


# region Login Account
def login_account(android_id):
    url = 'https://2ffe4.playfabapi.com/Client/LoginWithAndroidDeviceID'
    data = {
        "AndroidDevice": None,
        "AndroidDeviceId": android_id,
        "CreateAccount": True,
        "EncryptedRequest": None,
        "InfoRequestParameters": None,
        "OS": None,
        "PlayerSecret": None,
        "TitleId": "2FFE4",
        "AuthenticationContext": None
    }
    response = requests.post(url, json=data)
    session_ticket = None
    entity_token = None
    if response.status_code == 200:
        response = json.loads(response.content)
        if 'data' in response:
            if 'SessionTicket' in response['data']:
                session_ticket = response['data']['SessionTicket']
            if 'EntityToken' in response['data']:
                if 'EntityToken' in response['data']['EntityToken']:
                    entity_token = response['data']['EntityToken']['EntityToken']

        accounts = Table('accounts')
        query = PostgreSQLQuery.from_(accounts).select("username").where(accounts.android_id == android_id)
        query = str(query)
        username = database.get_query(query)[0]
        if username is not None:
            query = PostgreSQLQuery.update(accounts) \
                .set(accounts.session_ticket, session_ticket) \
                .set(accounts.entity_token, entity_token)
        query = str(query)
        database.set_query(query)


# endregion


# region Create Account
def create_account(_):
    android_id = secrets.token_hex(16)
    print("creating account..." + android_id)
    url = 'https://2ffe4.playfabapi.com/Client/LoginWithAndroidDeviceID'
    data = {
        "AndroidDevice": None,
        "AndroidDeviceId": android_id,
        "CreateAccount": True,
        "EncryptedRequest": None,
        "InfoRequestParameters": None,
        "OS": None,
        "PlayerSecret": None,
        "TitleId": "2FFE4",
        "AuthenticationContext": None
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        response = json.loads(response.content)
        username = du.generate_username()[0]
        session_ticket = response['data']['SessionTicket']
        entity_token = response['data']['EntityToken']['EntityToken']
        device_name = du.get_device()
        device_uid = du.get_uniqueid()
        device_os = du.get_os()
        device_gpu = du.get_gpu()
        device_cpu = du.get_cpu()
        playfab_id = response['data']['PlayFabId']
        entity_id = response['data']['EntityToken']["Entity"]["Id"]
        alchemy_time = (datetime.datetime.now() - (datetime.timedelta(days=2))).strftime("%m/%d/%Y %H:%M:%S %p")

        client_session_id = str(uuid.uuid4())
        focus_id = str(uuid.uuid4())

        device_token = ''.join(random.choice(string.ascii_letters + string.digits + "-_") for i in range(22)) \
                       + ":" + ''.join(random.choice(string.ascii_letters + string.digits + "-_") for i in range(140))

        accounts = Table('accounts')
        query = PostgreSQLQuery.into(accounts) \
            .insert(
            datetime.datetime.now(),
            android_id,
            username,
            session_ticket,
            entity_token,
            device_name,
            device_uid,
            device_os,
            device_gpu,
            device_cpu,
            playfab_id,
            entity_id,
            client_session_id,
            focus_id,
            device_token
        )
        query = str(query)
        database.set_query(query)

        report_device_info(device_name, device_uid, device_os, device_gpu, device_cpu, session_ticket)
        write_events(entity_id, playfab_id, device_name, device_os, client_session_id, focus_id, entity_token)
        android_device_push_notification_registration(device_token, session_ticket)
        update_user_data(alchemy_time, session_ticket)
        update_user_title_display_name(username, session_ticket)
        update_player_statics(5, session_ticket)

# endregion
