import spacy
import logging
import pandas as pd
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from database.db_connection import get_connection
from spacy.matcher import Matcher
from backend.services.nlp import nlp_pipeline # Registers the merge_vocab_phrases factory
from backend.services.nlp.vocabulary import (
    aesthetics, prints, colors, materials, fashion_brands, fashion_nouns, fashion_adjectives, fashion_collections, excluded_phrases
)

logger = logging.getLogger(__name__)

# Setting my local timezone for accurate trend collection and analysis (Change to ET or UTC!)
local_timezone = ZoneInfo("America/Denver")

class EntityExtractor:
    """Extract fashion entities from RSS articles using spaCy's NLP."""
    LABEL_TO_TYPE = {
    "FASHION_SEASON": "season",
    "COLLECTION_TYPE": "collection",
    "FASHION_BRAND": "brand",
    "MATERIAL": "material",
    "PRINT": "print",
    "AESTHETIC": "aesthetic",
    "COLOR": "color"
    }

    LABEL_TO_VOCAB = {
    "FASHION_BRAND": fashion_brands,
    "COLOR": colors,
    "MATERIAL": materials,
    "PRINT": prints,
    "AESTHETIC": aesthetics,
    "COLLECTION_TYPE": fashion_collections,
    "EXCLUDE": excluded_phrases,
    }

    # Initializing the object and defining its defaults.
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.matcher = self.define_matcher()
        self.entity_ruler = self.define_entity_ruler()    
        self.nlp.add_pipe("merge_vocab_phrases", last = True)
    
    # =================== Loading Articles by Date ===================
    def load_articles(self, target_date):
        """Load articles from the database for the target days."""
        
        try:
            query = """
                SELECT id, source_name, title, content, published_at
                FROM aggregates_trend
                WHERE published_at::date = %s
                ORDER BY published_at DESC
            """
            # TODO: LIMIT %s might be useful for preventing overloading

            with get_connection() as conn:
                data_frame = pd.read_sql(query, conn, params = (target_date,))

            data_frame["full_text"] = (data_frame["title"].fillna("") + " " + data_frame["content"].fillna("")).str.strip()

            logger.info("Loaded %d article(s) for date: %s.", len(data_frame), target_date)

            return data_frame
        
        except Exception as err:
            logger.error("Error loading articles for date %s: %s", target_date, err, exc_info = True)
            raise
    
    # =================== Define Matcher for Trend Detection ===================
    def define_matcher(self):
        """Build a matcher based on Part-of-Speech patterns and fashion vocabulary for detecting trends."""

        matcher = Matcher(self.nlp.vocab)
    
        # adjective + noun (oversized blazer)
        adj_noun = [
            {"LEMMA": {"IN": [fashion_adj.lower() for fashion_adj in fashion_adjectives]}},
            {"LEMMA": {"IN": [fashion_noun.lower() for fashion_noun in fashion_nouns]}}
        ]

        # material + noun (leather jacket)
        mat_noun = [
            {"LEMMA": {"IN": [material.lower() for material in materials]}},
            {"LEMMA": {"IN": [fashion_noun.lower() for fashion_noun in fashion_nouns]}}
        ]

        # material + adjective + noun (oversized leather jacket)
        mat_adj_noun = [
            {"LEMMA": {"IN": [fashion_adj.lower() for fashion_adj in fashion_adjectives]}},
            {"LEMMA": {"IN": [material.lower() for material in materials]}},
            {"LEMMA": {"IN": [fashion_noun.lower() for fashion_noun in fashion_nouns]}}
        ]

        # brand name + noun (gucci loafers)
        brand_noun = [
            {"LOWER": {"IN": [brand.lower() for brand in fashion_brands]}},
            {"LEMMA": {"IN": [fashion_noun.lower() for fashion_noun in fashion_nouns]}}
        ]

        # brand name + adjective + noun (gucci penny loafers)
        brand_adj_noun = [
            {"LOWER": {"IN": [brand.lower() for brand in fashion_brands]}},
            {"LEMMA": {"IN": [fashion_adj.lower() for fashion_adj in fashion_adjectives]}},
            {"LEMMA": {"IN": [fashion_noun.lower() for fashion_noun in fashion_nouns]}}
        ]

        matcher.add("FASHION_TREND", [adj_noun, mat_noun, mat_adj_noun, brand_noun, brand_adj_noun])

        return matcher

    # =================== Define Entity Ruler===================
    def define_entity_ruler(self):
        """Revised Entity Ruler patterns."""
        
        ruler = self.nlp.add_pipe("entity_ruler", before = "ner")

        # Fashion Seasons Entity Ruler Patterns
        fashion_seasons_pattern = [

            # ---------- Abbreviated Seasons ----------
            # One single token with no spaces: "SS26"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"REGEX": r"^(ss|aw|fw)\d{2,4}$"}}
                ]
            },

            # Abbreviated season with a slash and no spaces: "S/S26"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["s", "f", "a"]}},
                    {"TEXT": "/"},
                    {"LOWER": {"REGEX": r"^[sw]\d{2,4}$"}}
                ]
            },

            # Abbreviated season separated by a slash: "S/S 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["s", "f", "a"]}},
                    {"TEXT": "/"},
                    {"LOWER": {"IN": ["s", "w"]}},
                    {"TEXT": {"REGEX": r"^(20)?\d{2}$"}}
                ]
            },

            # Abbreviated season with no slash: "SS 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["ss", "fw", "aw"]}},
                    {"TEXT": {"REGEX": r"^(20)?\d{2}$"}}
                ]
            },

            # ---------- Pre-Collections ----------
            # Pre-collection variations: "Resort 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["resort", "cruise"]}},
                    {"TEXT": {"REGEX": r"^20\d{2}$"}}
                ]
            },

            # Pre-fall written as one word: "Prefall 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": "prefall"},
                    {"TEXT": {"REGEX": r"^20\d{2}$"}}
                ]
            },

            # Pre-fall with a space: "Pre Fall 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": "pre"},
                    {"LOWER": "fall"},
                    {"TEXT": {"REGEX": r"^20\d{2}$"}}
                ]
            },

            # Pre-fall with a hyphen or slash (spaCy splits it into three tokens): "Pre-Fall 2026", "Pre/Fall 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": "pre"},
                    {"TEXT": {"IN": ["/", "-"]}},
                    {"LOWER": "fall"},
                    {"TEXT": {"REGEX": r"^20\d{2}$"}}
                ]
            },

            # ---------- Full Season Names ----------
            # Full season name using a separator: "Spring/Summer 2026", "Fall-Winter 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["spring", "fall", "autumn"]}},
                    {"TEXT": {"IN": ["/", "-"]}},
                    {"LOWER": {"IN": ["summer", "winter"]}},
                    {"TEXT": {"REGEX": r"^20\d{2}$"}}
                ]
            },

            # Full season name and no separator: "Spring Summer 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["spring", "fall", "autumn"]}},
                    {"LOWER": {"IN": ["summer", "winter"]}},
                    {"TEXT": {"REGEX": r"^20\d{2}$"}}
                ]
            },

            # One single season and year: "Spring 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["spring", "summer", "autumn", "fall", "winter"]}},
                    {"TEXT": {"REGEX": r"^20\d{2}$"}}
                ]
            },

            # ---------- Year First Format ----------
            # Year and two season names: "2026 Spring/Summer"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^20\d{2}$"}},
                    {"LOWER": {"IN": ["spring", "fall", "autumn"]}},
                    {"TEXT": {"IN": ["/", "-"]}},
                    {"LOWER": {"IN": ["summer", "winter"]}}
                ]
            },

            # Year and single season name: "2026 Spring"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^20\d{2}$"}},
                    {"LOWER": {"IN": ["spring", "summer", "autumn", "fall", "winter"]}}
                ]
            },

            # Year and pre-collection: "2026 Resort"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^20\d{2}$"}},
                    {"LOWER": {"IN": ["resort", "cruise"]}}
                ]
            },

            # Year and pre-fall: "2026 Pre-Fall", "2026 Pre/Fall"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^20\d{2}$"}},
                    {"LOWER": "pre"},
                    {"TEXT": {"IN": ["/", "-"]}},
                    {"LOWER": "fall"}
                ]
            },
        ]

        patterns = [
            {"label": label, "pattern": term.lower()}
            for label, terms in self.LABEL_TO_VOCAB.items()
            for term in terms
        ]
        patterns += fashion_seasons_pattern
        ruler.add_patterns(patterns)
        return ruler

    def extract_article_entities(self, text):
        """ Extract article entities.
        
        Perform NLP analysis per articles served. Return the set of (entity_type, entity_value) pairs found in the text.
        
        Args:
            text: Full text of one article.
            
        Returns:
            entities: Set of (entity_type, entity_value) pairs.
        """
        try:
            if not text: 
                return set()
            
            doc = self.nlp(text)
            matches = self.matcher(doc)
            
            found_entities = set()

            for _, start, end in matches:
                span = doc[start:end]
                trend = span.lemma_
                found_entities.add(("trend", trend))

            for ent in doc.ents:
                entity_type = self.LABEL_TO_TYPE.get(ent.label_)
                if entity_type is not None:
                    found_entities.add((entity_type, ent.text))       

            logger.debug("Found %d entities in article: %s", len(found_entities), sorted(found_entities))
            
            return found_entities
            
        except Exception as err:    
            logger.error("Failed to extract article's entities: %s", err, exc_info = True)
            raise 

    def save_article_entities_to_database(self, article_id, entities, conn):
        """Replace one article's saved entities with the newly extracted ones.

            Deletes the article's existing rows and inserts the new ones in a single
            transaction, then commits. The caller owns the connection and closes it.

            Args:
                article_id: UUID of the article in aggregates_trend.
                entities: Set of (entity_type, entity_value) pairs.
                conn: Open psycopg connection.

            Returns:
                int: Number of rows saved.
         """
        try:
            rows = [(article_id, entity_type, value) for entity_type, value in entities]
            with conn.cursor() as cur:
                cur.execute("DELETE FROM article_entities WHERE article_id = %s", (article_id,))             
                cur.executemany("INSERT INTO article_entities (article_id, entity_type, entity_value) VALUES (%s, %s, %s)", rows)
            conn.commit()
            logger.debug("Saved %d entities for article %s.", len(rows), article_id)
            return len(rows)
        
        except Exception as err:
            conn.rollback()
            logger.error("Failed to save entities for article %s: %s", article_id, err, exc_info = True)
            raise
    
    def process_articles(self, data_frame, conn):
        """ Extract entities for every article in the DataFrame and save them. 
        
        Args:
            data_frame: Articles to process, with "id" and "full_text" columns.
            conn: Open psycopg connection.

        Returns:
            int: Number of articles processed.
        """
        article_count = 0
        articles_with_entities = 0
        total_entities = 0
        distinct_trends = set()

        try:
            for _, row in data_frame.iterrows():
                entities_found = self.extract_article_entities(row["full_text"])   
                self.save_article_entities_to_database(row["id"], entities_found, conn)

                article_count += 1
                total_entities += len(entities_found)
                if entities_found:
                    articles_with_entities += 1
                distinct_trends.update(value for entity_type, value in entities_found if entity_type == "trend")

            logger.info(
                "Processed %d article(s): %d with entities, %d entities saved, %d distinct trend(s).",
                article_count, articles_with_entities, total_entities, len(distinct_trends),
            )
            return article_count

        except Exception as err:
            logger.error("Extraction process failed: %s", err, exc_info = True)
            raise
    
    def backfill(self):     
        """ Backfill data from a specified date up to today.
        
        Pick every date from the start date to today, one day at a time, load articles, and call the processor.
        
        Args:
            None

        Returns:
            None
        """   
        try:
            processed_dates = 0
            total_articles = 0
            start_date =  date(2025, 11, 1)
            current_date = start_date
            end_date = datetime.now(local_timezone).date()     
            delta = timedelta(days = 1)

            logger.info("Starting backfill from %s to %s.", start_date, end_date)

            while current_date <= end_date:
                data_frame = self.load_articles(current_date)
                if len(data_frame) > 0:
                    logger.info("Processing current date: %s with total number of articles: %d.", current_date, len(data_frame))
                    with get_connection() as conn:
                        total_articles += self.process_articles(data_frame, conn)
                    
                    processed_dates += 1  

                else:
                    logger.debug("No articles found for date: %s.", current_date)      
                
                current_date += delta
            
            logger.info("Backfill process completed. Total number of dates processed: %d. Total number of articles processed: %d.", processed_dates, total_articles)
     
        except Exception as err:
            logger.error("Backfill process failed: %s", err, exc_info = True)
            raise

    def daily_analysis(self):
        """ Perform analysis for the specified date.
        
        Run the daily analysis, load articles and call the processor.
        
        Args:
            None

        Returns:
            None
        """
        try:
            today = datetime.now(local_timezone).date()
            data_frame = self.load_articles(today)
            with get_connection() as conn:
                count = self.process_articles(data_frame, conn)

                logger.info("Daily analysis completed successfully. Total number of articles processed: %d.", count)
                
        except Exception as err:
            logger.error("Daily analysis failed: %s", err, exc_info = True)
            raise
