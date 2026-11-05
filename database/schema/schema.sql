-- Fashion Data Vault: current database schema.
-- Reference only: describes how the database looks now.
-- Changes to an existing database go in database/migrations/, applied in order.

CREATE TABLE IF NOT EXISTS aggregates_trend (id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                                                                         source_type TEXT NOT NULL, -- Data source (RSS, Google Trends, Social APIs)
 source_name TEXT NOT NULL, -- Outlet (Vogue, Elle, Business of Fashion, ...)
 title TEXT NOT NULL,
            content TEXT, -- RSS teaser; full articles are not collected
 keywords TEXT[], link TEXT NOT NULL,
                            published_at TIMESTAMP, -- Original publish time, if available
 collected_at TIMESTAMP NOT NULL DEFAULT NOW(),
                                         metadata JSONB DEFAULT '{}', -- Source-specific data
 CONSTRAINT unique_source_link UNIQUE (source_name,
                                       link));

-- One row per (article, entity), so an entity counts once per article.
-- Re-extracting an article replaces its rows (delete, then insert).

CREATE TABLE IF NOT EXISTS article_entities
    (article_id UUID NOT NULL REFERENCES aggregates_trend (id) ON DELETE CASCADE,
                                                                         entity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                                                                                                            entity_type TEXT NOT NULL, -- trend, brand, season, material, color, aesthetic, collection
 entity_value TEXT NOT NULL,
                   extracted_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
                                                          CONSTRAINT unique_article_entities_values UNIQUE (article_id,
                                                                                                            entity_type,
                                                                                                            entity_value));


CREATE INDEX IF NOT EXISTS article_entities_lookup ON article_entities (entity_type, entity_value);

-- Daily counts for the API, computed from article_entities.
-- Replaced the old trend_summary table (migration 002).

CREATE OR REPLACE VIEW trend_summary AS
SELECT e.entity_type,
       e.entity_value,
       COUNT(*)::int AS count,
       a.published_at::date AS snapshot_date
FROM article_entities e
JOIN aggregates_trend a ON a.id = e.article_id
WHERE a.published_at IS NOT NULL
GROUP BY e.entity_type,
         e.entity_value,
         a.published_at::date;