import logging
import os

from dotenv import load_dotenv

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

REQUEST_DELAY_INTERVAL = 600  # request delay interval in seconds
LIMIT = 10  # limit of result list


DATABASE_NAME = 'currency_database.db'


load_dotenv()
TOKEN = os.getenv('TOKEN')  # telegram bot token
URL = os.getenv("URL")  # url for parsing data
USER_AGENT = os.getenv("USER_AGENT")
ACCEPT = os.getenv("ACCEPT")
HEADERS = {"User-Agent": USER_AGENT, "Accept": ACCEPT}
