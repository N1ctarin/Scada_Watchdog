import logging.config

logging.config.dictConfig('logging.json')
logger = logging.getLogger('DevLogger')

logger.info('Если на пути встают препятствия, попробуйте импортировать решения.')