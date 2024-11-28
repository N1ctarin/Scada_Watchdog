import json
import requests


class ScadaWatchdogNotification:

    def autorize(self):
        link = "https://iiot.ekfgroup.com/api/v1/auth/signin"
        with open('kredu.json', 'r') as config_file:
            config = json.load(config_file)
        email = config['email']
        password = config['password']

        body_for_request_auto = {"login":{"type":"EMAIL","value":email},"password":password}
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*', 'Connection': 'keep-alive', 'Content-Length': '85', 'Accept-Language': 'ru', 'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web'}
        request_for_login = requests.post(link, json=body_for_request_auto, headers=headers)

        status_code = request_for_login.status_code
        print(status_code)
        print(request_for_login.json())

        access_token_get = request_for_login.json()['data']['session']['accessToken']
        refresh_token_get = request_for_login.json()['data']['session']['refreshToken']
        print(access_token_get)
        return access_token_get, refresh_token_get

    def run_script_notifications(self, access_token):
        link = "https://iiot.ekfgroup.com/api/v1/scripts/2533/run"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Content-Length': '56', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web', 'Authorization': access_token}
        body_for_request = {'transactionId': "c8df1e87-c2a3-4767-b027-1f46b664ff63"}
        request_for_run_script = requests.post(link, headers=headers, json=body_for_request)
        print(request_for_run_script.status_code)

    def get_notifications_only_new(self, access_token):
        link = "https://iiot.ekfgroup.com/api/v1/notifications?projectId=282&state=NEW&page=1&size=30"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        request_for_get_notifications = requests.get(link, headers=headers)
        print(request_for_get_notifications.status_code)
        print(request_for_get_notifications.json()['data']['notifications'])
        return request_for_get_notifications.json()['data']['notifications']

    def check_status_notification(self, list_notifications_only_new, status):
        list_opt = list_notifications_only_new
        count = 0
        for notification in list_opt:
            if notification['severity'] == status: count += 1
        print(count)

        if count > 0: return True
        else: return False

    def read_notifications(self, access_token):
        link = "https://iiot.ekfgroup.com/api/v1/notifications/set-read-state"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Content-Length': '34', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        body = {"projectId": "282", "state": "READ"}
        request_for_read_notifications = requests.post(link, headers=headers, json=body)
        print(request_for_read_notifications.status_code, end=" ")
        print("notifications read")

