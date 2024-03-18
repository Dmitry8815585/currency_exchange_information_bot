import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

log_file = 'app.log'

max_file_size = 1024 * 1024 * 50  # 50 MB

file_handler = RotatingFileHandler(
    log_file, maxBytes=max_file_size, backupCount=3
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

REQUEST_DELAY_INTERVAL = 3600  # request delay interval in seconds
LIMIT = 10  # limit of result list
DATABASE_NAME = 'currency_database.db'
TOKEN = os.getenv('TOKEN')  # telegram bot token
URL = os.getenv("URL")  # url for parsing data
USER_AGENT = os.getenv("USER_AGENT")
ACCEPT = os.getenv("ACCEPT")
HEADERS = {"User-Agent": USER_AGENT, "Accept": ACCEPT}
