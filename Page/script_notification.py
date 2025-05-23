import json
from datetime import datetime, timedelta
import requests
import uuid
from Page.logs.page_logger import logger


class ScadaWatchdogNotification:

    def authorization(self):
        link = "https://iiot.ekfgroup.com/api/v1/auth/signin"
        with open('kredu.json', 'r') as config_file:
            config = json.load(config_file)
        email = config['email']
        password = config['password']
        access_token_get = ''
        refresh_token_get =''

        try:
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
        except Exception as e:
            logger.error(f" Error - authorization, Error - {e}", exc_info=True)
            requests.get(
                'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Не работает "Авторизация" в Connect Industry')

        return access_token_get, refresh_token_get

    def run_script(self, access_token, number):
        link = f"https://iiot.ekfgroup.com/api/v1/scripts/{number}/run"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*',
                       'Connection': 'keep-alive', 'Content-Length': '56', 'Accept-Language': 'ru',
                       'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web', 'Authorization': access_token}
        transaction_id = uuid.uuid4()
        body_for_request = {'transactionId': f"{transaction_id}"}
        status_code = 0
        try:
            request_for_run_script = requests.post(link, headers=headers, json=body_for_request)
            status_code = request_for_run_script.status_code
            if status_code != 204:
                logger.warning(f"Status_code - {status_code}, id_scripts - {transaction_id}, Error - Status_code", exc_info=True)
            else:
                logger.info(f"Status_code - {status_code}, id_scripts - {transaction_id}")
        except Exception as e:
            logger.warning(f"Status_code - {status_code}, id_scripts - {transaction_id}, Error - {e}", exc_info=True)

    def get_notifications_only_new(self, access_token):
        link = "https://iiot.ekfgroup.com/api/v1/notifications?projectId=282&state=NEW&page=1&size=30"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        try:
            request_for_get_notifications = requests.get(link, headers=headers)
            return request_for_get_notifications.json()['data']['notifications']
        except Exception as e:
            logger.error(f" Error - get_notifications, Error - {e}", exc_info=True)
            requests.get(
                'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Не работает запрос на новые уведомления')
            return 0

    def check_status_notification(self, list_notifications_only_new, status):
        flag = False
        for notification in list_notifications_only_new:
            if notification['severity'] == status:
                flag = True
                break

        if flag: return True
        return False

    def read_notifications(self, access_token):
        link = "https://iiot.ekfgroup.com/api/v1/notifications/set-read-state"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Content-Length': '34', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        body = {"projectId": "282", "state": "READ"}
        try:
            request_for_read_notifications = requests.post(link, headers=headers, json=body)
        except Exception as e:
            logger.error(f" Error - read_notifications, Error - {e}", exc_info=True)

    def get_group_tags_project(self, access_token, project_id):
        link = f"https://iiot.ekfgroup.com/api/v1/tags/by-node?componentNodeId={project_id}&verbose=true&page=1&size=30"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        try:
            response_group_tags_project = requests.get(link, headers=headers)
            return response_group_tags_project.json()['data']['tags']
        except Exception as e:
            logger.error(f" Error - get_group_tags_project, Error - {e}", exc_info=True)

    def check_status_tags(self, tags_before_scripts, tags_after_scripts):
        return True if tags_before_scripts[1]['value'] != tags_after_scripts[1]['value'] else False

    def get_message(self):
        link = "https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/getUpdates?chat_id=-1002336236273&offset=-1"
        try:
            response = requests.get(link)
        except Exception as e:
            logger.error(f" Error - get_message, Error - {e}", exc_info=True)
            response = 0

        try:
            date_text = ((response.json()['result'][0]['message']['text'].split('\n')[6]).replace('T', ' '))[:26]
            time_now = datetime.utcnow()
            time_respons = datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S.%f')
            time_difference = max(time_respons, time_now) - min(time_respons, time_now)
            if time_difference > timedelta(minutes=5):
                return False
            return True
        except:
            return 500

    def check_comparison_value_tags_for_notifications(self, access_token, desired_value):
        link = "https://iiot.ekfgroup.com/api/v1/tags/by-node?componentNodeId=1367&verbose=true&page=1&size=30"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        try:
            response_check_status_script_pre_run_script = requests.get(link, headers=headers)
            value_widget = int(response_check_status_script_pre_run_script.json()['data']['tags'][0]['value'])
            return True if value_widget == desired_value else False
        except Exception as e:
            logger.error(f" Error - check_script_pre_run_script, Error - {e}", exc_info=True)

    def check_value_tag(self, access_token, number_project, number_tag):
        link = f"https://iiot.ekfgroup.com/api/v1/tags/by-node?componentNodeId={number_project}&verbose=true&page=1&size=30"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        try:
            response_check_status_value_tag = requests.get(link, headers=headers)
            return response_check_status_value_tag.json()['data']['tags'][number_tag]['value']
        except Exception as e:
            logger.error(f" Error - check_value_tag, Error - {e}", exc_info=True)
            return 0


    def edit_value_tag(self, access_token, id_tag, value):
        link = f"https://iiot.ekfgroup.com/api/v1/tags/{id_tag}/value/edit"
        headers = {'Accept-Encoding': 'gzip, deflate, br', 'content-type': 'application/json', 'accept': '*/*',
                   'Connection': 'keep-alive', 'Content-Length': '34', 'Accept-Language': 'ru',
                   'x-device-id': '86ec768b-2144-4d5c-9db0-84259c0c6e00', 'x-platform': 'web',
                   'Authorization': access_token}
        body = {"value":f"{value}"}
        try:
            s = requests.post(link, headers=headers, json=body)
            if s.status_code != 200:
                logger.error(f" Error - edit_value_tag, Error - {s.status_code}", exc_info=True)
        except Exception as e:
            logger.error(f" Error - edit_value_tag, Error - {e}", exc_info=True)