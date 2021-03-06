import logging
import random
import string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"
