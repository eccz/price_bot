import logging


logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')
logging.debug('A Debug message')
logging.info('An INFO')
logging.warning('A WARNING')
logging.error('An ERROR')
logging.critical('a message of critical severity')
