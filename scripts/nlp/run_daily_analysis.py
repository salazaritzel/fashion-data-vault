from backend.shared.utils.logging_config import configure_logging
from backend.services.nlp.entity_extractor import EntityExtractor

configure_logging("nlp")

if __name__ == '__main__':
    """Daily analysis of collected articles to extract trends, seasons, collections, brands, and materials, and save results to the database."""
    extractor = EntityExtractor()
    extractor.daily_analysis()
    print("Daily analysis completed.")

