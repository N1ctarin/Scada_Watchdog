import time
from Page.script_notification import ScadaWatchdogNotification
import requests

def notification_warning_and_alarm():
    page = ScadaWatchdogNotification()
    access_token, refresh_token = page.authorization() # получили токены

    page.run_script(access_token, 2533) # выполнили скрипт с генерацией уведомления
    time.sleep(3)
    list_notifications_only_new = page.get_notifications_only_new(access_token) # запрос всех новых уведомлений
    have_notification_warning = page.check_status_notification(list_notifications_only_new, "WARNING") # наличие предупредительного уведомления
    page.read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

    page.run_script(access_token, 2533) # выполнили скрипт с генерацией уведомления
    time.sleep(3)
    list_notifications_only_new = page.get_notifications_only_new(access_token) # запрос всех новых уведомлений
    have_notification_alarm = page.check_status_notification(list_notifications_only_new, "ALARM") # наличие уведомления об ошибки
    page.read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

    page.run_script(access_token, 2533) # возвращаем скрипт в исходный статус

    #Flag = False
    if have_notification_warning == False:
        requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=(TEST)Не работают уведомления с параметром "Warning"')
    #else:
        #Flag = True

    if have_notification_alarm == False:
        requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=(TEST)Не работают уведомления с параметром "Alarm"')
    #else:
        #if Flag == True:
            #requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')


def notification_trigger_script():
    page = ScadaWatchdogNotification()
    access_token, refresh_token = page.authorization() # получили токены
    tags_before_scripts = page.get_group_tags_project(access_token, 1373)  # получили список тегов из папки "скрипты" перед скриптом
    time.sleep(5)
    page.run_script(access_token, 2538) # выполнили скрипт (первый)
    time.sleep(5)
    tags_after_scripts = page.get_group_tags_project(access_token, 1373) # получили список тегов из папки "скрипты" после скрипта
    result = page.check_status_tags(tags_before_scripts, tags_after_scripts) # Проверка значений тегов до выполнения скрипта и после

    if result == False:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text= Не работает триггер "По изменению тега" в сервисе "Скрипты". Посмотрите!!!')
    #else:
        #requests.get(
            #'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')


def check_telegram():
    page = ScadaWatchdogNotification()
    result = page.get_message()
    print(result)
    if result == False:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Не работает сервис отправки уведомлений в Telegram. Посмотрите!!!')
    elif result == 500:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Внимание.\nОшибка выполнения скрипта проверки уведомлений в Телеграм.')
    else:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')
notification_warning_and_alarm()
notification_trigger_script()
check_telegram()
