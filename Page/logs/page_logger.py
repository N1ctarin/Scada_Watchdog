import logging

# получение пользовательского логгера и установка уровня логирования
logger = logging.getLogger("run_script")
logger.setLevel(logging.DEBUG)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = logging.FileHandler("run_script.log", mode='a')
py_formatter = logging.Formatter('%(asctime)s – %(name)s – %(levelname)s – %(message)s')

# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
logger.addHandler(py_handler)