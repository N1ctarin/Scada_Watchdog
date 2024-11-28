from .Page.script_notification import *


access_token, refresh_token = autorize() # получили токены

run_script_notifications(access_token) # выполнили скрипт с генерацией уведомления
list_notifications_only_new = get_notifications_only_new(access_token) # запрос всех новых уведомлений
have_notification_warning = check_status_notification(list_notifications_only_new, "WARNING") # наличие предупредительного уведомления
read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

run_script_notifications(access_token) # выполнили скрипт с генерацией уведомления
list_notifications_only_new = get_notifications_only_new(access_token) # запрос всех новых уведомлений
have_notification_alarm = check_status_notification(list_notifications_only_new, "ALARM") # наличие уведомления об ошибки
read_notifications(access_token) # читаем все уведомления, что сбросить стаус "новые"

run_script_notifications(access_token) # возвращаем скрипт в исходный статус

