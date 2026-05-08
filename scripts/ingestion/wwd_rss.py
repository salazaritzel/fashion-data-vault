from backend.services.ingestion.adapters.rss.base_rss_adapter import Base_RSS_Adapter
from backend.shared.utils.logging_config import configure_logging

configure_logging("ingestion")

if __name__ == '__main__':
    adapter = Base_RSS_Adapter(
        source_name = "WWD",
        rss_link = 'https://wwd.com/custom-feed/recent-stories/'
    )

    saved = adapter.collect_feed()
    print(f"Completed: {saved} new entries saved from WWD.") # For debugging