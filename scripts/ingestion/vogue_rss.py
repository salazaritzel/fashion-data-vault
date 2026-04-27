from backend.services.ingestion.adapters.rss.base_rss_adapter import Base_RSS_Adapter
from backend.shared.utils.logging_config import configure_logging

configure_logging("ingestion")

if __name__ == '__main__':
    adapter = Base_RSS_Adapter(
        source_name = 'Vogue',
        rss_link = 'https://www.vogue.com/feed/rss'
    )

    saved = adapter.collect_feed()
    print(f'Completed: {saved} new entries saved from Vogue.') # For debugging