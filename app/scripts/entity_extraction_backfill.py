"""Backfill process of entity extraction."""
from app.utils.logging_config import configure_logging
from app.services.processing.entity_extractor import EntityExtractor

configure_logging()

if __name__ == '__main__':
    extractor = EntityExtractor()
    extractor.backfill()
    print("Backfill completed.")