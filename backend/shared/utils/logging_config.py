import logging

def configure_logging(service_name: str):
    """Configure event logging system for the application."""

    logging.basicConfig(
        encoding = "utf-8",
        level = logging.INFO,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(f'logs/{service_name}.log'),
            logging.StreamHandler()
        ]
    )