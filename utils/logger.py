import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for deeper logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)