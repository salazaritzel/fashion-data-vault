"""
    Extracts trends, seasons, brands, and materials from collected articles.
    Output: What is trending 
"""

# 1. Load articles from database (last 30/60/90 days)
# 2. Define season pattern for (EntityRuler)
# 3. Define brands pattern for (EntityRuler + default NER)
# 4. Define materials pattern for (EntityRuler)
# 5. Build the matcher patterns for detecting trends
# 6. Extract trends using (Matcher)
# 7. Extract brand, material, and season mentions (entity ruler, counter)
# *** Would like to correlate season & trends, season & designer & trend, season & designer & material 
# 6. Save results (either update articles table or create summary table)

# Output: Either:
# Option A: Update aggregates_trend with extracted keywords column
# Option B: Create a new trend_summary table with counts

import spacy
import pandas as pd
from datetime import datetime, timedelta
# import datetime
from database.db_connection import get_connection 
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from collections import Counter
from app.services.processing.vocabulary import materials, fashion_brands, fashion_nouns, fashion_adjectives


class EntityExtractor:
    """Extract fashion entities (seasons, brands, materials, trends) from articles using spaCy's NLP."""

    # Initializing the python object, defining defaults.
    def __init__(self, days: int = 30):
        self.data_frame = self.load_articles(days)
        self.nlp = spacy.load("en_core_web_md")
        self.matcher = self.define_matcher()
        self.define_entity_ruler()

    # =================== 1. Load articles from database (last 30/60/90 days) LOADING DATA FROM DATABASE ===================
    def load_articles(self, days):
        """Load articles from the database for the last n days."""
        
        interval_time = datetime.now() - timedelta(days=days)
      
        query = """
            SELECT id, source_name, title, content, published_at
            FROM aggregates_trend
            WHERE published_at > %s
            ORDER BY published_at DESC
        """
        # LIMIT %s might be useful for preventing overloading

        with get_connection() as conn:
            data_frame = pd.read_sql(query, conn, params = (interval_time,))

        data_frame["full_text"] = (data_frame["title"] + " " + data_frame["content"].fillna(""))
        
        print(f"Loaded {len(data_frame)} articles from the last {days} days.")
        
        return data_frame
    
    # =================== 5. Build a matcher for trend detection (Matcher) MATCHER SETUP FOR DETECTING TRENDS ===================
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
    
    # =================== 2, 3, 4 Extract seasons, brands, materials (Entity Ruler) ADD ENTITY RULER TO PIPELINE WITH DEFINED PATTERNS===================
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
                    {"LOWER": {"IN": ["spring", "summer", "autumn", "fall", "winter"]}}, # should i remove sm and w??
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

        # Brand Names Entity Ruler Patterns
        brands_pattern = [
            {"label": "FASHION_BRAND", "pattern": brand.lower()}
            for brand in fashion_brands
        ] 

        # Materials Entity Ruler Patterns
        materials_pattern = [
            {"label": "MATERIAL", "pattern": material.lower()}
            for material in materials
        ]

        # Adding the New Patterns to the Entity Rules
        ruler.add_patterns(fashion_seasons_pattern)
        ruler.add_patterns(brands_pattern)
        ruler.add_patterns(materials_pattern)
 
    # =================== 6. Extract trends using (Matcher) TREND EXTRACTION USING MATCHER ===================
    def extract_trends(self):
        """Run trend extraction over collected articles to identify trends."""
        trends = []
        
        for i, row in self.data_frame.iterrows():
            doc = self.nlp(row['full_text'])
            matches = self.matcher(doc)
            
            # Deduplicate. If trend appears more than once within the same article, we only count it once.
            found_trends = set()
            
            for match_id, start, end in matches:
                span = doc[start:end]
                trend_lemma = span.lemma_
                trend_raw = span.text
                found_trends.add((trend_lemma, trend_raw))
            
            # Add found trends from this article to the general list of trends
            for trend in found_trends:
                trends.append(trend)

        trend_counts = Counter(trend_lemma for trend_lemma, trend_raw in trends)
        return trend_counts

    # ******************** 7. Extract season, materials, and brand mentions using our enity ruler ********************
    def extract_entities(self):
        """Run the entity ruler over collected articles to count mentions of seasons, brands, and materials."""
        seasons_found = []
        collection_found = []  # TODO: consider combining with season entity for more granular insights
        brands_found = []
        materials_found = []

        # Dedup mentions within same article. Similar to how we did it with extract_trends().
        for i, row in self.data_frame.iterrows():
            text = row['full_text']   
            doc = self.nlp(text)

            seasons_mentioned = set()
            brands_mentioned = set()
            materials_mentioned = set()

            for ent in doc.ents:
                if ent.label_ == "FASHION_SEASON":
                    seasons_mentioned.add(ent.text)
                elif ent.label_ == "COLLECTION_TYPE":
                    collection_found.append(ent.text)
                elif ent.label_ == "FASHION_BRAND":
                    brands_mentioned.add(ent.text)
                elif ent.label_ == "MATERIAL":
                    materials_mentioned.add(ent.text)

            for season in seasons_mentioned:
                seasons_found.append(season)
            for brand in brands_mentioned: 
                brands_found.append(brand)
            for material in materials_mentioned:
                materials_found.append(material)

            # Print findings for current article
            if seasons_mentioned:
                print(f"Found season: {sorted(seasons_mentioned)} in article {i + 1}")
            if brands_mentioned:
                print(f"Found brand: {sorted(brands_mentioned)} in article {i + 1}")
            if materials_mentioned:
                print(f"Found material: {sorted(materials_mentioned)} in article {i + 1}")

        seasons_count = Counter(seasons_found)
        brands_count = Counter(brands_found)
        materials_count = Counter(materials_found)

        # Summary counts
        print("\n" + "="*50)
        print("TOP SEASONS")
        print("="*50)
        for season, count in seasons_count.most_common(50):
            label = "mention" if count <= 1 else "mentions"
            print(f"{season:25} {count:2} {label}")
        
        print("\n" + "="*50)
        print("TOP BRANDS")
        print("="*50)
        for brand, count in brands_count.most_common(50):
            label = "mention" if count <= 1 else "mentions"
            print(f"{brand:25} {count:2} {label}")
        
        print("\n" + "="*50)
        print("TOP MATERIALS")
        print("="*50)
        for material, count in materials_count.most_common(50):
            label = "mention" if count <= 1 else "mentions"
            print(f"{material:25} {count:2} {label}")
        
        return seasons_count, brands_count, materials_count        
        
# RUNNER FOR TESTING ******************
if __name__ == "__main__":
    extractor = EntityExtractor(10)
    trend_counts = extractor.extract_trends()
    season_count, brand_count, material_count = extractor.extract_entities()