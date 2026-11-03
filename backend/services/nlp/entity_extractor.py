import spacy
import logging
import pandas as pd
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from database.db_connection import get_connection
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from collections import Counter
# from backend.shared.utils.logging_config import configure_logging
from backend.services.nlp import nlp_pipeline
from backend.services.nlp.vocabulary import (
    aesthetics, colors, materials, fashion_brands, fashion_nouns, fashion_adjectives, fashion_collections
)


# configure_logging() # DELETE THIS BUT VERIFY
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
    "AESTHETIC": "aesthetic",
    "COLOR": "color"
    }

    # Initializing the object and defining its defaults.
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.matcher = self.define_matcher()
        self.entity_ruler = self.define_entity_ruler()    
        self.nlp.add_pipe("merge_vocab_phrases", last = True)
    
    # =================== Loading Articles by Date ===================
    def load_articles(self, date):
        """Load articles from the database for the last n days."""
        
        try:
            query = """
                SELECT id, source_name, title, content, published_at
                FROM aggregates_trend
                WHERE published_at::date = %s
                ORDER BY published_at DESC
            """
            # TODO: LIMIT %s might be useful for preventing overloading

            with get_connection() as conn:
                data_frame = pd.read_sql(query, conn, params = (date,))

            data_frame["full_text"] = (data_frame["title"].fillna("") + " " + data_frame["content"].fillna("")).str.strip()

            logger.info("Loaded %d article(s) for date: %s.", len(data_frame), date)

            return data_frame
        
        except Exception as err:
            logger.error("Error loading articles for date %s: %s", date, err, exc_info = True)
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

    # =================== Define Entity Ruler for Season, Brand, and Material Extraction ===================
    def define_entity_ruler(self):
        """Revised Entity Ruler patterns for seasons, brands, and materials."""
        
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

        # Aesthetics Pattern (boho-grunge, Y2K, clean girl)
        aesthetics_pattern = [
            {"label": "AESTHETIC", "pattern": aesthetic.lower()}
            for aesthetic in aesthetics
        ]

        # Brand Names Patterns
        brands_pattern = [
            {"label": "FASHION_BRAND", "pattern": brand.lower()}
            for brand in fashion_brands
        ] 

        # Color Patterns
        colors_pattern = [
            {"label": "COLOR", "pattern": color.lower()}
            for color in colors
        ]

        # Fashion Collection Patterns
        fashion_collections_pattern = [
            {"label": "COLLECTION_TYPE", "pattern": fashion_collection.lower()}
            for fashion_collection in fashion_collections
        ]

        # Materials Patterns
        materials_pattern = [
            {"label": "MATERIAL", "pattern": material.lower()}
            for material in materials
        ]

        # TODO: Adding the new patterns to the entity ruler REDO MORE CLEANLY
        ruler.add_patterns(fashion_seasons_pattern)
        ruler.add_patterns(brands_pattern)
        ruler.add_patterns(colors_pattern)
        ruler.add_patterns(materials_pattern)
        ruler.add_patterns(aesthetics_pattern)
        ruler.add_patterns(fashion_collections_pattern)
        return ruler

    def extract_article_entities(self, text):
        """ Extract article entities per article served.
        
        Perform NLP analysis per articles served. Return the set of (entity_type, entity_value) pairs found in the text.
        
        Args:
            text: Full text of one article.
            
        Returns:
            entities: Set of (entity_type, entity_value) pairs.
        """
        try:
            if text is None: 
                return set()
            
            doc = self.nlp(text)
            matches = self.matcher(doc)
            
            found_entities = set()

            for _, start, end in matches:
                span = doc[start:end]
                trend = span.lemma_
                found_entities.add(("trend", trend))
            # print([(ent.text, ent.label_) for ent in doc.ents])    

            for ent in doc.ents:
                entity_type = self.LABEL_TO_TYPE.get(ent.label_)
                if entity_type is not None:
                    found_entities.add((entity_type, ent.text))       

            # logger.info("Article entities successfully extracted. Total number of entities extracted: %d from %d article(s).", article_count)

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
        
        For whatever articles it's handed: extract, then save.
        
        Args:
            data_frame: The text from the article. 
            conn: Open psycopg connection.

        Returns:
            int: Number of articles processed.
        """
        article_count = 0
        try:
            for _, row in data_frame.iterrows():
                entities_found = self.extract_article_entities(row["full_text"])
        
                self.save_article_entities_to_database(row["id"], entities_found, conn)
                article_count += 1

            logger.debug("Articles analyzed: %d", article_count)
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
            start_date =  date(2026, 10, 16)
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

    # =================== Extract Trends ===================
    def extract_trends(self, data_frame = None):
        """Run trend extraction over collected articles to identify trends."""
        
        print(f"Running trend extraction on {len(data_frame) if data_frame is not None else len(self.data_frame)} articles.")
        try:
            if data_frame is None: 
                data_frame = self.data_frame

            trends = []

            for i, row in data_frame.iterrows():
                doc = self.nlp(row['full_text'])
                matches = self.matcher(doc)

                # If trend appears more than once within the same article, we only count it once.
                found_trends = set()
                
                for match_id, start, end in matches:
                    span = doc[start:end]
                    trend_lemma = span.lemma_
                    trend_raw = span.text
                    found_trends.add((trend_lemma, trend_raw)) 
                    # print(f"Matched trend: {span.text}")
                 
                # Add found trends from this article to the general list of trends
                for trend in found_trends:
                    trends.append(trend)

            # trends_dic = {}
            # for trend_lemma, trend_raw in trends:
            #     if trend_lemma not in trends_dic:
            #         trends_dic[trend_lemma] = trend_raw

            trend_counts = Counter(
                trend_lemma for trend_lemma, trend_raw in trends
            )

            logger.info("Extracted %d unique trend(s) from %d article(s).", len(trend_counts), len(data_frame))
                
            return trend_counts
        
        except Exception as err:
            logger.error("Failed to extract trends: %s", err, exc_info = True)
            raise

    # =================== Extract Entities =================== NOTE: This needs to be improved, too many repetition, many nested loops
    def extract_entities(self, data_frame = None): # REDO this function, too long and repetitive.
        """Run the entity ruler over collected articles to count mentions of seasons, collections, brands, and materials."""

        try:
            if data_frame is None: 
                data_frame = self.data_frame

            seasons_found = []
            collection_found = []
            brands_found = []
            materials_found = []
            aesthetics_found = []
            colors_found = []

            # Dedup mentions within same article. Similar to how we did it with extract_trends()
            for i, row in data_frame.iterrows():
                text = row['full_text']   
                doc = self.nlp(text)

                seasons_mentioned = set()
                collection_mentioned = set()
                brands_mentioned = set()
                materials_mentioned = set()
                aesthetics_mentioned = set()
                colors_mentioned = set()

                for ent in doc.ents:
                    if ent.label_ == "FASHION_SEASON":
                        seasons_mentioned.add(ent.text)
                    elif ent.label_ == "COLLECTION_TYPE":
                        collection_mentioned.add(ent.text)
                    elif ent.label_ == "FASHION_BRAND":
                        brands_mentioned.add(ent.text)
                    elif ent.label_ == "MATERIAL":
                        materials_mentioned.add(ent.text)
                    elif ent.label_ == "AESTHETIC":
                        aesthetics_mentioned.add(ent.text)
                    elif ent.label_ == "COLOR":
                        colors_mentioned.add(ent.text)

                for season in seasons_mentioned:
                    seasons_found.append(season)
                for collection in collection_mentioned:
                    collection_found.append(collection)
                for brand in brands_mentioned: 
                    brands_found.append(brand)
                for material in materials_mentioned:
                    materials_found.append(material)
                for aesthetic in aesthetics_mentioned:
                    aesthetics_found.append(aesthetic)
                for color in colors_mentioned:
                    colors_found.append(color)

                # Debug print statements, delete later ******************
                # if seasons_mentioned:
                #     print(f"Found season: {seasons_mentioned} in article {i + 1} : {row['full_text']}") 

                # elif brands_mentioned:
                #     print(f"Found brand: {brands_mentioned} in article {i + 1} : {row['full_text']}")

                # elif materials_mentioned:
                #     print(f"Found material: {materials_mentioned} in article {i + 1} : {row['full_text']}")

            seasons_count = Counter(seasons_found)
            collections_count = Counter(collection_found)
            brands_count = Counter(brands_found)
            materials_count = Counter(materials_found) 
            aesthetics_count = Counter(aesthetics_found)
            colors_count = Counter(colors_found)

            logger.info("Extracted %d unique season(s), %d unique collection(s), %d unique brand(s), %d unique material(s), %d color(s), and %d unique aesthetic(s) from %d article(s).", 
                        len(seasons_count), len(collections_count), len(brands_count), len(materials_count), len(colors_count), len(aesthetics_count), len(data_frame))
            
            return seasons_count, collections_count, brands_count, materials_count, colors_count, aesthetics_count

        except Exception as err:    
            logger.error("Failed to extract entities: %s", err, exc_info = True)
            raise 

    # ================ Save Results to Database ================
    def save_results_to_database(self, trend_counts, season_counts, collection_counts, brand_counts, material_counts, color_counts, aesthetic_counts, snapshot_date = None):
        """Save extracted trends, seasons, collections, brands, and materials to the database."""

        try:
            if snapshot_date is None:
                snapshot_date = datetime.now(local_timezone).date() # Use today for the snapshot date 
        
            query = """
                INSERT INTO trend_summary 
                    (entity_type, entity_value, count, snapshot_date)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (entity_type, entity_value, snapshot_date) DO NOTHING
                RETURNING id;
            """
            
            entities = {
                "trend": trend_counts,
                "season": season_counts,
                "collection": collection_counts,
                "brand": brand_counts,
                "material": material_counts,
                "aesthetic": aesthetic_counts,
                "color": color_counts
            }

            saved_count = 0
            duplicate_count = 0   
            with get_connection() as conn:
                with conn.cursor() as cur:
                    for entity_type, entity_counts in entities.items():
                        for entity_value, count in entity_counts.items():
                            # print(f"Entity Type is: {entity_type} | Entity Value is: {entity_value} | Count is: {count} | Time Window is: {time_window} days |\n Snapshot Date is {datetime.now().date()})

                            cur.execute(query, (
                                entity_type,
                                entity_value,
                                count,
                                snapshot_date
                            ))

                            result = cur.fetchone()

                            if result:
                                saved_count += 1
                                logger.debug("Saved %s, value %s with count %d.", entity_type, entity_value, count)
                            else:
                                duplicate_count += 1
                                logger.debug("Duplicate entry for %s, value %s. Skipping insertion.", entity_type, entity_value)

                        conn.commit()
                    
                    logger.info("Finished saving results to database for date %s. New entries saved: %s. Duplicates skipped: %s.", snapshot_date, saved_count, duplicate_count)
            
            return saved_count
        
        except Exception as err:
            logger.error("Failed to save results to database: %s", err, exc_info = True)
            raise



    # =================== Backfilling Data (Pick every date from the start date to today, one day at a time) ===================
    # def backfill(self):

    #     # backfill
    #     # for each date from start_date to end_date:
    #     #     df = self.load_articles(current_date)
    #     #     if len(df) > 0:
    #     #         with get_connection() as conn:
    #     #             self.process_articles(df, conn)

    #     try:
    #         start_date =  date(2026, 10, 16)
    #         end_date = datetime.now(local_timezone).date()
    #         for date in range(start_date, end_date):
    #             df = self.load_articles(date)
    #             logger.info("Starting backfill from %s to %s.", start_date, end_date)
    #             processed_dates = 0
    #             if len(df) > 0:
    #                 logger.info("Processing current date: %s with total number of articles: %d.", date, len(df))
    #                 with get_connection() as conn:
    #                     self.process_articles(df, conn)   
    #             else:
    #                 logger.debug("No articles found for date: %s.", date)
            
    #         logger.info("Backfill process completed. Total number of dates processed: %d.", processed_dates)
        
    #     except Exception as err:
    #         logger.error("Backfill process failed: %s", err, exc_info = True)
    #         raise

        # try:
        #     start_date =  date(2026, 10, 16) # Starting from November 1st (anything prior is too scattered) (i reaaaally need to setup a cron job)
        #     # start_date = datetime.now(local_timezone).date() - timedelta(days = 1) # For testing, backfill the last 5 days
        #     current_date = start_date
        #     end_date = datetime.now(local_timezone).date() # Backfill up to today (4/15/26)

        #     # Using timedelta to increment our current date by one day per iteration until we reach end date
        #     delta = timedelta(days = 1)

        #     logger.info("Starting backfill from %s to %s.", start_date, end_date)
        #     processed_dates = 0 # For debugging delete after

        #     while current_date <= end_date:
        #         df = self.load_articles(current_date)
        #         if len(df) > 0:
        #             logger.info("Processing current date: %s with total number of articles: %d.", current_date, len(df))
        
        #             trend_counts = self.extract_trends(df)
        #             season_counts, collection_counts, brand_counts, material_counts, color_counts, aesthetic_counts = self.extract_entities(df)
        #             self.save_results_to_database(trend_counts, season_counts, collection_counts, brand_counts, material_counts, color_counts, aesthetic_counts, snapshot_date = current_date)
        #             processed_dates += 1     
        #         else:
        #             logger.debug("No articles found for date: %s.", current_date)      
                
        #         current_date += delta
            
        #     logger.info("Backfill process completed. Total number of dates processed: %d.", processed_dates)
        
        # except Exception as err:
        #     logger.error("Backfill process failed: %s", err, exc_info = True)
            # raise

    # # =================== Daily Analysis (Pick today’s articles) ===================
    # def daily_analysis(self):
    #     """Run daily analysis: load articles, extract trends and entities, and save results to the database."""      

    #     # daily_analysis
    #     # today = ...
    #     # df = self.load_articles(today)
    #     # with get_connection() as conn:
    #     #     self.process_articles(df, conn)

    #     try:
    #         today = datetime.now(local_timezone).date()
    #         data_frame = self.load_articles(today)
    #         with get_connection() as conn:
    #             entities = self.process_articles(data_frame, conn)   
    #             self.save_article_entities_to_database(article_id, entities, conn)
    #             logger.info("Daily analysis completed successfully.")
    #     except Exception as err:
    #         logger.error("Daily analysis failed: %s", err, exc_info = True)
    #         raise

        # try:
        #     today = datetime.now(local_timezone).date()
        #     data_frame = self.load_articles(today)
        #     trend_counts = self.extract_trends(data_frame)
        #     season_counts, collection_counts, brand_counts, material_counts, color_counts, aesthetic_counts = self.extract_entities(data_frame)
        #     self.save_results_to_database(trend_counts, season_counts, collection_counts, brand_counts, material_counts, color_counts, aesthetic_counts, snapshot_date = today)
        #     logger.info("Daily analysis completed successfully.")
        # except Exception as err:
        #     logger.error("Daily analysis failed: %s", err, exc_info = True)
        #     raise