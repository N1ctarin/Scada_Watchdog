import json
from datetime import datetime, timedelta
import requests
import uuid


class ScadaWatchdogNotification:

    def authorization(self):
        link = "https://iiot.ekfgroup.com/api/v1/auth/signin"
        with open('kredu.json', 'r') as config_file:
            config = json.load(config_file)
        email = config['email']
        password = config['password']

        body_for_request_auto = {"login":{"type":"EMAIL","value":email},"password":password}
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*', 'Connection': 'keep-alive', 'Content-Length': '85', 'Accept-Language': 'ru', 'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web'}
        request_for_login = requests.post(link, json=body_for_request_auto, headers=headers)
        id_aut = request_for_login.json()['data']['otp']['id']

        link = "https://iiot.ekfgroup.com/api/v1/otp/verify"
        body = {"transactionId": id_aut, "otp": "0000"}
        request_for_verify = requests.post(link, json=body, headers=headers)
        token = request_for_verify.json()['data']['verification']['token']

        link = "https://iiot.ekfgroup.com/api/v1/auth/signin/verify"
        body = {"verificationToken": token}
        request_for_verify_2 = requests.post(link, json=body, headers=headers)

        access_token_get = request_for_verify_2.json()['data']['session']['accessToken']
        refresh_token_get = request_for_verify_2.json()['data']['session']['refreshToken']
        return access_token_get, refresh_token_get

    def run_script(self, access_token, number):
        random_uuid = uuid.uuid4()
        link = f"https://iiot.ekfgroup.com/api/v1/scripts/{number}/run"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Content-Length': '56', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web', 'Authorization': access_token}
        body_for_request = {'transactionId': f"{random_uuid}"}
        request_for_run_script = requests.post(link, headers=headers, json=body_for_request)

    def get_notifications_only_new(self, access_token):
        link = "https://iiot.ekfgroup.com/api/v1/notifications?projectId=282&state=NEW&page=1&size=30"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        request_for_get_notifications = requests.get(link, headers=headers)
        return request_for_get_notifications.json()['data']['notifications']

    def check_status_notification(self, list_notifications_only_new, status):
        flag = False
        for notification in list_notifications_only_new:
            if notification['severity'] == status:
                flag = True
                break

        if flag: return True
        else: return False

    def read_notifications(self, access_token):
        link = "https://iiot.ekfgroup.com/api/v1/notifications/set-read-state"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Content-Length': '34', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        body = {"projectId": "282", "state": "READ"}
        request_for_read_notifications = requests.post(link, headers=headers, json=body)

    def get_group_tags_project(self, access_token, project_id):
        link = f"https://iiot.ekfgroup.com/api/v1/tags/by-node?componentNodeId={project_id}&verbose=true&page=1&size=30"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        response_group_tags_project = requests.get(link, headers=headers)
        return response_group_tags_project.json()['data']['tags']

    def check_status_tags(self, tags_before_scripts, tags_after_scripts):
        if tags_before_scripts[1]['value'] != tags_after_scripts[1]['value']:
            return True
        else:
            return False

    def get_message(self):
        link = "https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/getUpdates?chat_id=-1002336236273&offset=-1"
        response = requests.get(link)
        try:
            id_bot_from_telegram = response.json()['result'][0]['message']['forward_from']['id']
            date_text = ((response.json()['result'][0]['message']['text'].split('\n')[6]).replace('T', ' '))[:26]
            time_now = datetime.utcnow()
            time_respons = datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S.%f')
            print(response.json())
            print(id_bot_from_telegram)
            print(date_text)
            print(time_now)
            time_difference = max(time_respons, time_now) - min(time_respons, time_now)
            print(time_difference)
            if time_difference > timedelta(minutes=5):
                return False
            else:
                return True
        except:
            return 500



