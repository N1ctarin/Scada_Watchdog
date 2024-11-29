from Page.script_notification import ScadaWatchdogNotification
import requests

page = ScadaWatchdogNotification()

access_token, refresh_token = page.authorization() # получили токены

page.run_script_notifications(access_token) # выполнили скрипт с генерацией уведомления
list_notifications_only_new = page.get_notifications_only_new(access_token) # запрос всех новых уведомлений
have_notification_warning = page.check_status_notification(list_notifications_only_new, "WARNING") # наличие предупредительного уведомления
page.read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

page.run_script_notifications(access_token) # выполнили скрипт с генерацией уведомления
list_notifications_only_new = page.get_notifications_only_new(access_token) # запрос всех новых уведомлений
have_notification_alarm = page.check_status_notification(list_notifications_only_new, "ALARM") # наличие уведомления об ошибки
page.read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

page.run_script_notifications(access_token) # возвращаем скрипт в исходный статус

Flag = False
if have_notification_warning == False:
    requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Не работают уведомления с параметром "Warning"(ТЕСТ)')
else:
    Flag = True

if have_notification_alarm == False:
    requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Не работают уведомления с параметром "Alarm"(ТЕСТ)')
else:
    if Flag == True:
        requests.get('https://api.telegram.org/bot7205176061:AAGjERufx2q-IAsbHCIAMKEBeHrVyo9lJMo/sendMessage?chat_id=-4503284662&text=Автоматический прогон. Не обращайте внимание')

