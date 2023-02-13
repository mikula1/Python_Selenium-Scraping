import logging

main_file_logger = logging.FileHandler('logs/main.log')
main_file_logger.setFormatter(logging.Formatter('%(asctime)s : %(name)s : %(message)s'))
main_file_logger.setLevel(logging.INFO)

error_file_logger = logging.FileHandler('logs/error.log')
error_file_logger.setFormatter(logging.Formatter('%(asctime)s : %(name)s : %(message)s'))
error_file_logger.setLevel(logging.ERROR)

logger = logging.getLogger('scraper_v1')
# set the level of logger high, so it would not filter out messages for each handler.
logger.setLevel(logging.DEBUG)
logger.addHandler(error_file_logger)
logger.addHandler(main_file_logger)