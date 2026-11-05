CREATE TABLE IF NOT EXISTS article_entities (
    article_id UUID NOT NULL REFERENCES aggregates_trend (id) ON DELETE CASCADE,
    entity_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type TEXT NOT NULL,
    entity_value TEXT NOT NULL,
    extracted_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    CONSTRAINT unique_article_entities_values UNIQUE (article_id, entity_type, entity_value)
);

CREATE INDEX IF NOT EXISTS article_entities_lookup ON article_entities (entity_type, entity_value);