import time
from Page.script_notification import ScadaWatchdogNotification
import requests

def notification_warning_and_alarm():
    page = ScadaWatchdogNotification()
    access_token, refresh_token, id_aut = page.authorization() # получили токены

    page.run_script(access_token, 2533, id_aut) # выполнили скрипт с генерацией уведомления
    list_notifications_only_new = page.get_notifications_only_new(access_token) # запрос всех новых уведомлений
    have_notification_warning = page.check_status_notification(list_notifications_only_new, "WARNING") # наличие предупредительного уведомления
    page.read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

    page.run_script(access_token, 2533, id_aut) # выполнили скрипт с генерацией уведомления
    list_notifications_only_new = page.get_notifications_only_new(access_token) # запрос всех новых уведомлений
    have_notification_alarm = page.check_status_notification(list_notifications_only_new, "ALARM") # наличие уведомления об ошибки
    page.read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

    page.run_script(access_token, 2533, id_aut) # возвращаем скрипт в исходный статус

    Flag = False
    if have_notification_warning == False:
        requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=(TEST)Не работают уведомления с параметром "Warning"(ТЕСТ)')
    else:
        Flag = True

    if have_notification_alarm == False:
        requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=(TEST)Не работают уведомления с параметром "Alarm"(ТЕСТ)')
    else:
        if Flag == True:
            requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')


def notification_trigger_script():
    page = ScadaWatchdogNotification()
    access_token, refresh_token, id_aut = page.authorization() # получили токены
    tags_before_scripts = page.get_group_tags_project(access_token, 1373)  # получили список тегов из папки "скрипты" перед скриптом
    time.sleep(2)
    page.run_script(access_token, 2538, id_aut) # выполнили скрипт (первый)
    time.sleep(2)
    tags_after_scripts = page.get_group_tags_project(access_token, 1373) # получили список тегов из папки "скрипты" после скрипта
    result = page.check_status_tags(tags_before_scripts, tags_after_scripts) # Проверка значений тегов до выполнения скрипта и после
    print(result)

    if result:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')
    else:
        requests.get(
            'https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=(TEST) Не работает триггер "По изменению тега" в сервисе "Скрипты". Посмотрите!!!')

notification_warning_and_alarm()
#notification_trigger_script()