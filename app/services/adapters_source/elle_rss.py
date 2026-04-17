import logging
from app.services.adapters_source.base_rss_adapter import Base_RSS_Adapter
from app.utils.logging_config import configure_logging

# Configure logger
# logging.basicConfig(
#     encoding = 'utf-8',
#     level = logging.INFO,
#     format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers = [
#         logging.FileHandler('logs/scraper.log'),
#         logging.StreamHandler()
#     ]
# )

configure_logging()

if __name__ == '__main__':
    adapter = Base_RSS_Adapter(
        source_name = "Elle",
        rss_link = 'https://www.elle.com/rss/all.xml'
    )

    saved = adapter.collect_feed()
    print(f"Completed: {saved} new entries saved from Elle.") # For debugging