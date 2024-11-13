import json
import requests

link = "https://iiot.ekfgroup.com/api/v1/auth/signin"


#@pytest.fixture
def autotize():
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

    access_token = request_for_login.json()['data']['session']['accessToken']
    refresh_token = request_for_login.json()['data']['session']['refreshToken']
    print(access_token)


autotize()
