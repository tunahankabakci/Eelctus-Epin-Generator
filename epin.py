import csv
import json
import time

import requests
from pypika import PostgreSQLQuery

from database import get_query_all
from electus import get_user_data


def use_epin(cookie, data_token, epin):
    url = 'https://electus.online/activate/epin'
    data = {
        "_token": data_token,
        "epin": epin
    }
    headers = {
        "cookie": cookie
    }
    return requests.post(url, data=data, headers=headers)


def use_all_epin_from_csv(cookie, data_token):
    file = open("csv_files/epin2.csv")
    epins = csv.reader(file)
    epins = list(epins)
    for epin in epins:
        epin = epin[0]
        response = use_epin(cookie, data_token, epin)
        start = response.text.find("You have successfully activated the EPin!")
        gift = response.text[start:]
        start = gift.find("received")
        start = start + 9
        end = gift.find("Electus Cash") - 1
        silk_count = gift[start:end]
        print(epin + "    *********    " + silk_count)
        time.sleep(0.2)


def get_epins_from_all_accounts():
    query = PostgreSQLQuery.from_('accounts').select('android_id')
    query = str(query)
    android_ids = get_query_all(query)
    for android_id in android_ids:
        url = 'https://2ffe4.playfabapi.com/Client/LoginWithAndroidDeviceID'
        data = {
            "AndroidDevice": None,
            "AndroidDeviceId": android_id[0],
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
            if 'data' in response:
                if 'SessionTicket' in response['data']:
                    session_ticket = response['data']['SessionTicket']
                    response_temp = get_user_data(session_ticket)
                    response_temp = json.loads(response_temp.content)
                    if 'data' in response_temp:
                        if 'Data' in response_temp['data']:
                            if 'lastepin' in response_temp['data']['Data']:
                                if 'Value' in response_temp['data']['Data']['lastepin']:
                                    epin = response_temp['data']['Data']['lastepin']['Value']
                                    if epin != "":
                                        if epin != " ":
                                            print(epin)


def get_epins_from_account(android_id):
    print('.')
    url = 'https://2ffe4.playfabapi.com/Client/LoginWithAndroidDeviceID'
    data = {
        "AndroidDevice": None,
        "AndroidDeviceId": android_id[0],
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
        if 'data' in response:
            if 'SessionTicket' in response['data']:
                session_ticket = response['data']['SessionTicket']
                response_temp = get_user_data(session_ticket)
                response_temp = json.loads(response_temp.content)
                if 'data' in response_temp:
                    if 'Data' in response_temp['data']:
                        if 'lastepin' in response_temp['data']['Data']:
                            if 'Value' in response_temp['data']['Data']['lastepin']:
                                epin = response_temp['data']['Data']['lastepin']['Value']
                                if epin != "":
                                    if epin != " ":
                                        print(epin)