import logging

# получение пользовательского логгера и установка уровня логирования
logger = logging.getLogger("run_script")
logger.setLevel(logging.DEBUG)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_handler = logging.FileHandler("default.log", mode='a')
py_formatter = logging.Formatter('%(asctime)s – %(name)s – %(levelname)s – %(message)s')

# добавление форматировщика к обработчику
py_handler.setFormatter(py_formatter)
# добавление обработчика к логгеру
logger.addHandler(py_handler)


# получение пользовательского логгера и установка уровня логирования
logger_default = logging.getLogger("default")
logger_default.setLevel(logging.DEBUG)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
default_handler = logging.FileHandler("default.log", mode='a')
default_formatter = logging.Formatter('%(asctime)s – %(name)s – %(levelname)s – %(message)s')

# добавление форматировщика к обработчику
default_handler.setFormatter(default_formatter)
# добавление обработчика к логгеру
logger_default.addHandler(default_handler)