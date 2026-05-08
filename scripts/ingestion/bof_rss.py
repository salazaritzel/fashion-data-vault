from backend.services.ingestion.adapters.rss.base_rss_adapter import Base_RSS_Adapter
from backend.shared.utils.logging_config import configure_logging

configure_logging("ingestion")

if __name__ == '__main__':
    adapter = Base_RSS_Adapter(
        source_name = 'Business of Fashion',
        rss_link = 'https://www.businessoffashion.com/arc/outboundfeeds/rss/?outputType=xml'
    )

    saved = adapter.collect_feed()
    print(f'Completed: {saved} new entries saved from Business of Fashion.') # For debugging