"""Daily analysis of collected articles to extract trends, seasons, collections, brands, and materials, and save results to the database."""
from app.utils.logging_config import configure_logging
from app.services.processing.entity_extractor import EntityExtractor

configure_logging()

if __name__ == '__main__':
    extractor = EntityExtractor(days = 1) # Running daily. We only want to analyze the articles collected in the past day.
    extractor.daily_analysis()

