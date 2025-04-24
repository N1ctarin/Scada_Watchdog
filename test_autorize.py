import time
from Page.logs.page_logger import logger_default
from Page.script_notification import ScadaWatchdogNotification
import requests

def notification_warning_and_alarm():
    page = ScadaWatchdogNotification()
    access_token, refresh_token = page.authorization() # получили токены

    counter_fault_write_valume_in_tag = 0
    for i in range(6): # Проверка исходных значений в теге (парсит значение на дашборде) - лучше отрефакторить
        status_script = page.check_comparison_value_tags_for_notifications(access_token, 0)
        if status_script:
            page.read_notifications(access_token)
            break
        else:
            page.edit_value_tag(access_token, 6593, 0)
            time.sleep(2)
            counter_fault_write_valume_in_tag += 1

    page.edit_value_tag(access_token, 6593, 17)
    time.sleep(3) # техническое ожидание, чтоб данные успели обновиться в тегах
    list_notifications_only_new = page.get_notifications_only_new(access_token) # запрос всех новых уведомлений
    have_notification_warning = page.check_status_notification(list_notifications_only_new, "WARNING") # наличие предупредительного уведомления
    page.read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

    for i in range(6): # Проверка исходных значений в теге (парсит значение на дашборде) - лучше отрефакторить
        status_script = page.check_comparison_value_tags_for_notifications(access_token, 17)
        if status_script:
            page.read_notifications(access_token)
            break
        else:
            page.edit_value_tag(access_token, 6593, 17)
            time.sleep(2)
            counter_fault_write_valume_in_tag += 1

    if counter_fault_write_valume_in_tag >= 5:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Внимание.\nОшибка записи значения в тег')

    page.edit_value_tag(access_token, 6593, 25)
    time.sleep(3) # техническое ожидание, чтоб данные успели обновиться в тегах
    list_notifications_only_new = page.get_notifications_only_new(access_token) # запрос всех новых уведомлений
    have_notification_alarm = page.check_status_notification(list_notifications_only_new, "ALARM") # наличие уведомления об ошибки
    page.read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"
    page.edit_value_tag(access_token, 6593, 0)

    #Flag = False
    if not have_notification_warning:
        requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Не работают уведомления с параметром "Warning"')
    #else:
        #Flag = True

    if not have_notification_alarm:
        requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Не работают уведомления с параметром "Alarm"')
    #else:
        #if Flag == True:
            #requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')


def check_trigger_script():
    page = ScadaWatchdogNotification()
    access_token, refresh_token = page.authorization() # получили токены
    tags_before_scripts = page.get_group_tags_project(access_token, 1373)  # получили список тегов из папки "скрипты" перед скриптом
    time.sleep(1) # техническое ожидание, чтоб данные успели обновиться в тегах
    now_value_tag_for_run_script = page.check_value_tag(access_token, 1373, 0) # запоминаем текущее значения в теге
    if now_value_tag_for_run_script == "false":
        value = "true"
    else:
        value = "false"
    page.edit_value_tag(access_token, 6600, value)
    time.sleep(3)
    tags_after_scripts = page.get_group_tags_project(access_token, 1373) # получили список тегов из папки "скрипты" после скрипта
    result = page.check_status_tags(tags_before_scripts, tags_after_scripts) # Проверка значений тегов до выполнения скрипта и после

    if not result:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text= Не работает триггер "По изменению тега" в сервисе "Скрипты". Посмотрите!!!')
    #else:
        #requests.get(
            #'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')


def check_telegram():
    page = ScadaWatchdogNotification()
    result = page.get_message()
    if not result:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Не работает сервис отправки уведомлений в Telegram. Посмотрите!!!')
    elif result == 500:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Внимание.\nОшибка выполнения скрипта проверки уведомлений в Телеграм.')
    #else:
    #    requests.get(
    #        'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')


logger_default.info("START")
notification_warning_and_alarm()
check_trigger_script()
check_telegram()
logger_default.info("FINISH")