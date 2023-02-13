import sys
import  logging

err_num = 18
print('{} : {}'.format('No internet connection', err_num), file=open("logs/error.log", "a+"))

sys.stderr.write("err 115511")

formatter = logging.Formatter('%(asctime)s : %(name)s : %(message)s')

error_file_logger = logging.FileHandler('logs/error.log')
error_file_logger.setFormatter(formatter)
error_file_logger.setLevel(logging.ERROR)

# error_logger = logging.getLogger(__name__)
# error_logger.setLevel(logging.ERROR)
# error_logger.addHandler(error_file_logger)


main_file_logger = logging.FileHandler('logs/main.log')
main_file_logger.setFormatter(formatter)
main_file_logger.setLevel(logging.INFO)

# main_logger = logging.getLogger(__name__)
# main_logger.setLevel(logging.INFO)
# main_logger.addHandler(main_file_logger)

# logging.basicConfig(filename="logs/app.log", level=logging.INFO,format="%(asctime)s :%(name)s :%(message)s")
# logging.info("Program started")
#
logger = logging.getLogger("login")
logger.setLevel(logging.INFO)
logger.addHandler(error_file_logger)
logger.addHandler(main_file_logger)

logger.error("ERROR")
logger.info("INFO")
logger.warning("WARNING")
