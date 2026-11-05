-- Replace the old count table with a view computed from article_entities.
-- The API in backend/services/api/main.py reads it unchanged.
-- Rollback:
--   DROP VIEW trend_summary;
--   ALTER TABLE trend_summary_old RENAME TO trend_summary;

BEGIN;

ALTER TABLE trend_summary RENAME TO trend_summary_old;

CREATE VIEW trend_summary AS
SELECT
    e.entity_type,
    e.entity_value,
    COUNT(*)::int AS count,
    a.published_at::date AS snapshot_date
FROM article_entities e
JOIN aggregates_trend a ON a.id = e.article_id
WHERE a.published_at IS NOT NULL
GROUP BY e.entity_type, e.entity_value, a.published_at::date;

COMMIT;