from backend.shared.utils.logging_config import configure_logging
from backend.services.nlp.entity_extractor import EntityExtractor

configure_logging("nlp")

if __name__ == '__main__':
    """Backfill process of entity extraction."""
    extractor = EntityExtractor()
    extractor.backfill()
    print("Backfill completed.")