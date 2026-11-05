-- Fashion Data Vault: schema for the tables this project uses.

-- One row per collected article (title + RSS teaser; full articles are not collected).
CREATE TABLE IF NOT EXISTS aggregates_trend (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type  TEXT NOT NULL,           -- Data source (RSS, Google Trends, Social APIs)
    source_name  TEXT NOT NULL,           -- Outlet (Vogue, Elle, Business of Fashion, ...)
    title        TEXT NOT NULL,
    content      TEXT,                    -- RSS teaser
    keywords     TEXT[],
    link         TEXT NOT NULL,
    published_at TIMESTAMP,               -- Original publish time, if available
    collected_at TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata     JSONB DEFAULT '{}',      -- Source-specific data
    CONSTRAINT unique_source_link UNIQUE (source_name, link)
);

-- One row per (article, entity), so an entity counts once per article.
-- Re-extracting an article replaces its rows (delete, then insert, in one transaction).
CREATE TABLE IF NOT EXISTS article_entities (
    article_id   UUID NOT NULL REFERENCES aggregates_trend (id) ON DELETE CASCADE,
    entity_id    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type  TEXT NOT NULL,           -- trend, brand, season, material, color, ...
    entity_value TEXT NOT NULL,
    extracted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_article_entities_values UNIQUE (article_id, entity_type, entity_value)
);

CREATE INDEX IF NOT EXISTS article_entities_lookup
    ON article_entities (entity_type, entity_value);

-- Deprecated: replaced by article_entities. No longer written to or read by the API. Pending drop.
CREATE TABLE IF NOT EXISTS trend_summary (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type   TEXT NOT NULL,
    entity_value  TEXT NOT NULL,
    count         INTEGER NOT NULL,
    snapshot_date DATE NOT NULL,
    created_at    TIMESTAMP DEFAULT NOW(),
    CONSTRAINT unique_values UNIQUE (entity_type, entity_value, snapshot_date)
);