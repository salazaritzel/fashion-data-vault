import logging
from app.services.adapters_source.base_rss_adapter import Base_RSS_Adapter
from app.utils.logging_config import configure_logging

configure_logging()

if __name__ == '__main__':
    adapter = Base_RSS_Adapter(
        source_name = 'Business of Fashion',
        rss_link = 'https://www.businessoffashion.com/arc/outboundfeeds/rss/?outputType=xml'
    )

    saved = adapter.collect_feed()
    print(f'Completed: {saved} new entries saved from Business of Fashion.') # For debugging