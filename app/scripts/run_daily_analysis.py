"""Daily analysis of collected articles to extract trends, seasons, collections, brands, and materials, and save results to the database."""
from app.utils.logging_config import configure_logging
from app.services.processing.entity_extractor import EntityExtractor

configure_logging()

if __name__ == '__main__':
    extractor = EntityExtractor()
    extractor.daily_analysis()

