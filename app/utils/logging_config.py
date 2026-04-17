import logging

def configure_logging():
    """Configure event logging system for the application."""

    logging.basicConfig(
        encoding = "utf-8",
        level = logging.INFO,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler('logs/scraper.log'),
            logging.StreamHandler()
        ]
    )