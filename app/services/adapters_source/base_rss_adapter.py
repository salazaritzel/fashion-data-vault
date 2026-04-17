import re
import json
import logging
import psycopg
import feedparser
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from bs4 import BeautifulSoup
from database.db_connection import get_connection

# Set up the logger for event tracking
logger = logging.getLogger(__name__)

class Base_RSS_Adapter:
    """
    Base adapter for RSS feed collection.

    ETL Pipeline: fetch -> validate -> clean -> save
    """
    def __init__(self, source_name: str, rss_link: str):
        self.source_name = source_name
        self.rss_link = rss_link
        logger.info('Initializing RSS adapter for %s', source_name)

#############################################################################################################################         
    def fetch_feed(self):
        """Fetch RSS feed from the source."""
        try:
           feed = feedparser.parse(self.rss_link)

           # Detecting a non-well-formed feed using bozo detection
           if feed.bozo:
               logger.warning('Feed may be malformed for %s: %s', self.source_name, feed.bozo_exception)
         
           return feed

        except Exception as err:
            logger.error('Failed to fetch feed from %s: %s', self.source_name, err, exc_info = True)
            
            return None

# What are type hints and should i write them?? Would it look elegant???
#############################################################################################################################         
    def validate_entry(self, entry):
        """Validate a single entry. Ensures required fields exist."""
        title = entry.get('title', '').strip()
        link = entry.get('link', '').strip()
        summary = entry.get('summary', '')

        # Validate link format
        if not link.startswith(('https://', 'http://')):
            logger.debug('Invalid link format: %s', link)
            return None
        
        # Skip entry if it's missing required fields
        if not title or not link:
            logger.debug('Missing required fields.')
            return None

        if len(title) < 3:
            logger.debug('Title is too short: %s', title)
            return None
        
        return {
            'title': title[:500],
            'link': link[:2048],
            'summary': summary[:5000] if summary else None,
            'published': entry.get('published'),
            'author': entry.get('author', '')
        }

#############################################################################################################################         
    def validate_entries(self, feed):
        """Validate all entries in the field.""" 
        if not feed or not feed.entries:
            logger.warning('RSS feed has no entries or failed to parse for %s', self.source_name)
            return []
        
        valid_entries = []

        try:
            for entry in feed.entries:
                validated = self.validate_entry(entry)
                if validated:
                    valid_entries.append(validated)
        
        except Exception as err:
            logger.error('Iteration error during validation for %s: %s', self.source_name, err, exc_info = True)
        
        if valid_entries:
            logger.info('Validated %d out of %d entries successfully for %s', len(valid_entries), len(feed.entries), self.source_name)
        else:
            logger.warning('No valid entries found for %s', self.source_name)

        return valid_entries

#############################################################################################################################         
    def clean_text(self, raw_text):
        """Clean and sanitize text."""
        if not raw_text: 
            return None
        
        try:    
            # Decode HTML entities
            text = unescape(raw_text)
            
            # Strip all html tags using lxml instead of html.parser for speed
            text = BeautifulSoup(text, 'lxml').get_text()

            # Convert text to lower case to unify fashion entities (prada, Prada, PRADA). Important for accurate keyword count.
            text = text.lower()

            # Normalize any white space within the text
            text = re.sub(r'\s+', ' ', text).strip()

            return text if text else None
        
        except Exception as err:
            logger.warning('Text cleaning error: %s', err)
            return None

#############################################################################################################################         
    def parse_date(self, date_str):
        """Parse RSS date string to datetime object for accurate TIMESTAMP insertion."""
        if not date_str:
            return None
        
        try:
            return parsedate_to_datetime(date_str)
        
        except (TypeError, ValueError) as err:
            logger.warning('Failed to parse date %s: %s', date_str, err)
            return None
    
#############################################################################################################################         
    def normalize_entries(self, entries):
        """
        Normalize validated entries into database format.
        Cleans text and structures entry data for PostgreSQL insertion.
        """
        normalized_data = []

        for entry in entries:
            try:
                title = self.clean_text(entry.get('title', ''))
                content = self.clean_text(entry.get('summary', ''))

                normalized_entry = {
                    'source_type': 'RSS',
                    'source_name': self.source_name,
                    'title': title,
                    'content': content,
                    'keywords': None,
                    'link': entry.get('link', ''),
                    'published_at': self.parse_date(entry.get('published')),
                    'collected_at': datetime.now(timezone.utc),
                    'metadata': {'author': entry.get('author', '')}
                    }
                
                normalized_data.append(normalized_entry)
                
            except Exception as err:
                logger.warning('Error normalizing entry: %s', err)
                continue # Continue with the rest of the entries

        logger.info('Normalized %d out of %d entries for %s', len(normalized_data), len(entries), self.source_name)

        return normalized_data

#############################################################################################################################  
    def save_to_database(self, entries_list):
        """Store multiple entries into PostgreSQL database."""
        if not entries_list:
            logger.info('No entries to save for %s', self.source_name)
            return 0

        # Build the query prior to inserting it into the database
        # Use parameterized queries to prevent SQL injection attacks
        # TO-DO: Change all single quotes to double quotes. It's better practice. Also added semicolon to return id.
        query = '''
            INSERT INTO aggregates_trend
                (source_type, source_name, title, content, keywords,
                link, published_at, collected_at, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (source_name, link) DO NOTHING
            RETURNING id;
        '''
        
        saved_count = 0

        try:
            # Connect to the database using the get_connection() import
            with get_connection() as conn:
                # Open a cursor to perform database operations
                with conn.cursor() as cur:
                    for entry in entries_list:
                        try:
                            cur.execute(query, (
                                entry['source_type'],
                                entry['source_name'],
                                entry['title'],
                                entry['content'],
                                entry['keywords'],
                                entry['link'],
                                entry['published_at'],
                                entry['collected_at'],
                                json.dumps(entry['metadata']),
                            ))

                            result = cur.fetchone() # Returns one row as a tuple from the query result

                            if result:
                                saved_count += 1
                                logger.debug('Saved entry: %s (ID: %s)', entry['title'][:50], result[0])
                            else:
                                logger.debug('Duplicate skipped: %s', entry['link'])

                        except psycopg.Error as err:
                            logger.warning('Failed to insert entry %s: %s', entry['link'], err)
                            continue # Continue inserting the next entry

                    conn.commit() # Commit any pending transaction to the database

            logger.info('Batch save complete for %s. %d entries saved.', self.source_name, saved_count)
            
            return saved_count
                    
        except psycopg.Error as err:
            logger.error('Database connection failed for %s: %s', self.source_name, err, exc_info = True)
            return 0
        
        except Exception as err:
            logger.exception('Unexpected error during batch save for %s: %s', self.source_name, err)
            return 0

#############################################################################################################################         
    def collect_feed(self):
        """
        Main data collection pipeline for RSS feeds: fetch -> validate -> clean -> normalize -> save
        When we run the separate source files (vogue, wwd, bof) this is our entry point. The orchestrator.
        """    
        logger.info('Starting collection for feed %s from: %s', self.source_name, self.rss_link)

        # Surround with try and except blocks, log. But do i need to log if i am logging in each function?
        # Initially fetch the feed
        feed = self.fetch_feed()
        if not feed.get('entries'):
            logger.warning('No entries fetched for %s', self.source_name)
            return 0
        
        # Validate & Clean
        valid_entries = self.validate_entries(feed)
        if not valid_entries:
            logger.warning('No valid entries for %s', self.source_name)
            return 0
            
        # Normalize
        normalized_entries = self.normalize_entries(valid_entries)
        if not normalized_entries:
            logger.warning('No normalized entries for %s', self.source_name)
            return 0
        
        # Save to database
        saved_count = self.save_to_database(normalized_entries)
        logger.info('Collection and saving to database complete for %s. Processed a total of %d entries.', self.source_name, len(normalized_entries))

        return saved_count
    
# Data will be from fashion news articles. Extract the data, clean it and store it in PostgreSQL.
# There are a few ways to parse through an XML document, what I found was feedparser and plump. 
# Going to start with feedparser since its more stable.

# ALGORITHM
# CONNECT TO THE DATABASE:
# try and get the connection
# if it fails, fail gracefully with information
# We're doing this in a separate file, db_connection.py.

# GET THE DATA FROM THE RSS FEEDS:
# Try to fetch the data
# Validate the incoming data
# Sanitize the incoming data
# Store data into the database