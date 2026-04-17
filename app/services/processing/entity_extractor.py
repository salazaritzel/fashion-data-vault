import spacy
import logging
import pandas as pd
from datetime import date, datetime, timedelta, timezone
from database.db_connection import get_connection 
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from collections import Counter
from app.utils.logging_config import configure_logging
from app.services.processing.vocabulary import materials, fashion_brands, fashion_nouns, fashion_adjectives

configure_logging()
logger = logging.getLogger(__name__)

class EntityExtractor:
    """Extract fashion entities (seasons, collections, brands, materials, trends) from articles using spaCy's NLP."""

    # Initializing the python object, defining defaults.
    def __init__(self, days: int = 1):
        self.days = days
        self.data_frame = self.load_articles(days)
        self.nlp = spacy.load("en_core_web_md")
        self.matcher = self.define_matcher()
        self.entity_ruler = self.define_entity_ruler()

    # =================== Loading Articles from Database ===================
    def load_articles(self, days):
        """Load articles from the database for the last n days."""
        try:
            interval_time = datetime.now(timezone.utc) - timedelta(days=days)
           
            query = """
                SELECT id, source_name, title, content, published_at
                FROM aggregates_trend
                WHERE published_at > %s
                ORDER BY published_at DESC
            """
            # TODO: LIMIT %s might be useful for preventing overloading

            with get_connection() as conn:
                data_frame = pd.read_sql(query, conn, params = (interval_time,))
                
            data_frame["full_text"] = (data_frame["title"] + " " + data_frame["content"].fillna(""))
            
            logger.info("Loaded %d article(s) from the last %d day(s)", len(data_frame), days)
        
            return data_frame
        
        except Exception as err:
            logger.error("Failed to load articles for %d days: %s", days, err, exc_info = True)
            raise
        
    
    # =================== Loading Articles by Date (Backfilling) ===================
    # Where target date would be either today or November 1, 2025
    def load_articles_by_date(self, target_date):
        """One time job to back fill all our current saved data."""
        try:
            query = """
                SELECT id, source_name, title, content, published_at
                FROM aggregates_trend
                WHERE published_at::date = %s
                ORDER BY published_at DESC
            """

            with get_connection() as conn:
                df = pd.read_sql(query, conn, params = (target_date,))

            df["full_text"] = (df["title"] + " " + df["content"].fillna(""))

            logger.info("Loaded %d article(s) for date: %s.", len(df), target_date)
            
            return df
        
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
    
    # =================== Define Entity Ruler for Season, Brand, and Material Extraction ===================
    def define_entity_ruler(self):
        """Revised Entity Ruler patterns for seasons, brands, and materials."""
        
        ruler = self.nlp.add_pipe("entity_ruler", before = "ner") # Wrap around if else statements

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
      
            # One single token with slashes, no spaces: "S/S26"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^[SFA]$"}},
                    {"TEXT": "/"}, # "/"
                    {"TEXT": {"REGEX": r"^[SW]\d{2,4}$"}}
                ]
            },
            
            # Abbreviated season separated by a slash: "S/S 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["s", "f", "a"]}},
                    {"TEXT": {"IN": "/"}},
                    {"LOWER": {"IN": ["s", "w"]}},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },

            # Abbreviated season with no slash: "SS 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["ss", "fw", "aw"]}},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },

            # ---------- Pre-Collections ----------
            # Pre-collection variations: "Resort 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["resort", "cruise"]}},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },

            # Pre-Fall as a single token
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": "pre-fall"},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },

            # Pre-fall with space: "Pre Fall 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": "pre"},
                    {"LOWER": "fall"},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },

            # Pre-fall tokenized as three tokens: "Pre / Fall 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": "pre"},
                    {"TEXT": "-"},
                    {"LOWER": "fall"},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },

            # ---------- Full Season Names ----------
            # Full season name using separator: "Spring/Summer 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["spring", "summer", "autumn", "fall", "winter"]}}, # TODO:Review this pattern. Should I remove summer and winter??
                    {"TEXT": {"IN": ["/", "-"]}},
                    {"LOWER": {"IN": ["summer", "winter"]}},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },

            # Full season name and no separator: "Spring Summer 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["spring", "summer", "autumn", "fall", "winter"]}},
                    {"LOWER": {"IN": ["summer", "winter"]}},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },
            
            # One single season and year: "Spring 2026"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"LOWER": {"IN": ["spring", "summer", "autumn", "fall", "winter"]}},
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}}
                ]
            },

            # ---------- Year First Format ----------
            # Year and two season name: "2026 Spring/Summer"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}},
                    {"LOWER": {"IN": ["spring", "summer", "autumn", "fall", "winter"]}},
                    {"TEXT": {"IN": ["/", "-"]}},
                    {"LOWER": {"IN": ["summer", "winter"]}}
                ]
            },

            # Year and single season name: "2026 Spring"
            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}},
                    {"LOWER": {"IN": ["spring", "summer", "autumn", "fall", "winter"]}}
                ]
            },

            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}},
                    {"LOWER": {"IN": ["resort", "cruise"]}},
                ]
            },

            {
                "label": "FASHION_SEASON",
                "pattern": [
                    {"TEXT": {"REGEX": r"^\d{2,4}$"}},
                    {"LOWER": {"IN": "pre"}},
                    {"TEXT": {"IN": "/"}},
                    {"LOWER": {"IN": "fall"}}
                ]
            },

            # ---------- Collection Types ----------
            {"label": "COLLECTION_TYPE", "pattern": "Haute Couture"},
            {"label": "COLLECTION_TYPE", "pattern": "haute couture"},
            {"label": "COLLECTION_TYPE", "pattern": "Couture"},
            {"label": "COLLECTION_TYPE", "pattern": "couture"},
            {"label": "COLLECTION_TYPE", "pattern": "Ready-to-Wear"},
            {"label": "COLLECTION_TYPE", "pattern": "ready-to-wear"},
            {"label": "COLLECTION_TYPE", "pattern": "Womenswear"},
            {"label": "COLLECTION_TYPE", "pattern": "womenswear"},
            {"label": "COLLECTION_TYPE", "pattern": "Menswear"},
            {"label": "COLLECTION_TYPE", "pattern": "menswear"}
        ]

        # Brand Names Patterns
        brands_pattern = [
            {"label": "FASHION_BRAND", "pattern": brand.lower()}
            for brand in fashion_brands
        ] 

        # Materials Patterns
        materials_pattern = [
            {"label": "MATERIAL", "pattern": material.lower()}
            for material in materials
        ]

        # Adding the new patterns to the entity ruler
        ruler.add_patterns(fashion_seasons_pattern)
        ruler.add_patterns(brands_pattern)
        ruler.add_patterns(materials_pattern)
        
        return ruler
    
    # =================== Extract Trends ===================
    def extract_trends(self, data_frame = None):
        """Run trend extraction over collected articles to identify trends."""
        try:
            if data_frame is None: 
                data_frame = self.data_frame

            trends = []
            
            for i, row in data_frame.iterrows():
                doc = self.nlp(row['full_text'])
                matches = self.matcher(doc)
                
                # Deduplicate. If trend appears more than once within the same article, we only count it once.
                found_trends = set()
                
                for match_id, start, end in matches:
                    span = doc[start:end]
                    trend_lemma = span.lemma_
                    trend_raw = span.text
                    # print(f"Trend (lemma): '{trend_lemma}'")
                    # print(f"Trend (raw): '{trend_raw}'")
                    found_trends.add((trend_lemma, trend_raw)) 
                    
                    # Add found trends from this article to the general list of trends
                    for trend in found_trends:
                        trends.append(trend)
                
            # if found_trends:
            #     print(f"Found trends: {set(trend_raw for trend_lemma, trend_raw in found_trends)} in article {i + 1} : {row['full_text']}") 
        
            # Hmmmm.... I need to decide what I'm going to do here.
            # trends_dic = {}
            # for trend_lemma, trend_raw in trends:
            #     if trend_lemma not in trends_dic:
            #         trends_dic[trend_lemma] = trend_raw

            trend_counts = Counter(trend_lemma for trend_lemma, trend_raw in trends)

            logger.info("Extracted %d unique trend(s) from %d article(s).", len(trend_counts), len(data_frame))
                
            return trend_counts # trend_dic
        
        except Exception as err:
            logger.error("Failed to extract trends: %s", err, exc_info = True)
            raise

    # =================== Extract Entities ===================
    def extract_entities(self, data_frame = None):
        """Run the entity ruler over collected articles to count mentions of seasons, collections, brands, and materials."""

        try:
            if data_frame is None: 
                data_frame = self.data_frame

            seasons_found = []
            collection_found = []
            brands_found = []
            materials_found = []

            # Dedup mentions within same article. Similar to how we did it with extract_trends()
            for i, row in data_frame.iterrows():
                text = row['full_text']   
                doc = self.nlp(text)

                seasons_mentioned = set()
                collection_mentioned = set()
                brands_mentioned = set()
                materials_mentioned = set()

                for ent in doc.ents:
                    if ent.label_ == "FASHION_SEASON":
                        seasons_mentioned.add(ent.text)
                    elif ent.label_ == "COLLECTION_TYPE":
                        collection_mentioned.add(ent.text)
                    elif ent.label_ == "FASHION_BRAND":
                        brands_mentioned.add(ent.text)
                    elif ent.label_ == "MATERIAL":
                        materials_mentioned.add(ent.text)

                for season in seasons_mentioned:
                    seasons_found.append(season)
                for collection in collection_mentioned:
                    collection_found.append(collection)
                for brand in brands_mentioned: 
                    brands_found.append(brand)
                for material in materials_mentioned:
                    materials_found.append(material)

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

            logger.info("Extracted %d unique season(s), %d unique collection(s), %d unique brand(s), and %d unique material(s) from %d article(s).", 
                        len(seasons_count), len(collections_count), len(brands_count), len(materials_count), len(data_frame))
            
            return seasons_count, collections_count, brands_count, materials_count   

        except Exception as err:    
            logger.error("Failed to extract entities: %s", err, exc_info = True)
            raise 

    # ================ Save Results to Database ================
    def save_results_to_database(self, trend_counts, season_counts, collection_counts, brand_counts, material_counts, snapshot_date = None):
        """Save extracted trends, seasons, collections, brands, and materials to the database."""

        try:
            if snapshot_date is None:
                snapshot_date = datetime.now(timezone.utc).date() # Use today for the snapshot date 
        
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
                "material": material_counts
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


    # =================== Backfilling Data ===================
    def backfill(self):
        try:
            start_date =  date(2025, 11, 1) # Starting from November 1st (anything prior is too scattered)
            # start_date = datetime.now(timezone.utc).date() - timedelta(days = 3) # For testing, backfill the last 5 days
            current_date = start_date
            end_date = datetime.now(timezone.utc).date() # Backfill up to today (4/15/26)

            # Using timedelta to increment our current date by one day per iteration until we reach end date
            delta = timedelta(days = 1)

            logger.info("Starting backfill from %s to %s.", start_date, end_date)
            processed_dates = 0 # For debugging delete after

            while current_date <= end_date:
                df = self.load_articles_by_date(current_date)
                if len(df) > 0:
                    logger.info("Processing current date: %s with total number of articles: %d.", current_date, len(df))
        
                    trend_counts = self.extract_trends(df)
                    season_counts, collection_counts, brand_counts, material_counts = self.extract_entities(df)
                    self.save_results_to_database(trend_counts, season_counts, collection_counts, brand_counts, material_counts, snapshot_date = current_date)
                    processed_dates += 1     
                else:
                    logger.debug("No articles found for date: %s.", current_date)      
                
                current_date += delta
            
            logger.info("Backfill process completed. Total number of dates processed: %d.", processed_dates)
        
        except Exception as err:
            logger.error("Backfill process failed: %s", err, exc_info = True)
            raise

    # =================== Daily Analysis ===================
    def daily_analysis(self):
        """Run daily analysis: load articles, extract trends and entities, and save results to the database."""
        try:
            trend_counts = self.extract_trends()
            season_counts, collection_counts, brand_counts, material_counts = self.extract_entities()
            self.save_results_to_database(trend_counts, season_counts, collection_counts, brand_counts, material_counts)
            logger.info("Daily analysis completed successfully.")
        except Exception as err:
            logger.error("Daily analysis failed: %s", err, exc_info = True)
            raise