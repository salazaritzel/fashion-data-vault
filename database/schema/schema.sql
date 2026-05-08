-- SQL SCRIPTS

DROP TABLE IF EXISTS aggregates_trend;

-- V2 Normalizing data - centralized table for aggregated trends

CREATE TABLE aggregates_trend (id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                                                           source_type TEXT NOT NULL, -- Data source (RSS, Google Trends, Social APIs)
 source_name TEXT NOT NULL, -- Data name (Vogue, Google, Pinterest)
 title TEXT NOT NULL, -- Headline or title
 content TEXT, -- Full text if available
 keywords TEXT[], -- Extracted fashion trend keywords
 link TEXT NOT NULL, -- CHANGED Link back to the original source
 published_at TIMESTAMP, -- Original publish time (if available)
 collected_at TIMESTAMP NOT NULL DEFAULT NOW(), -- Time when it was fetched
 metadata JSONB DEFAULT '{}', -- For storing source specific data
 CONSTRAINT unique_source_link UNIQUE(source_name, link) -- Prevent duplicates
);

-- Creating a new table to track the counts of trends, seasons, brands, and material mentions.

CREATE TABLE IF NOT EXISTS trend_summary (id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                                                                      entity_type TEXT NOT NULL, -- trend, season, brand, material
 entity_value TEXT NOT NULL, -- if trend: leather jacket, if season: FW2026, etc.
 count INTEGER NOT NULL, -- but what if there's no count, well if there were not then it wouldnt even be here
 snapshot_date DATE NOT NULL, -- The date that this summary is for (kind of like published date (remember we're doing daily snapshots now which prevents overlaps and is overall cleaner))
 created_at TIMESTAMP DEFAULT NOW(), -- when this record was created
 CONSTRAINT unique_values UNIQUE(entity_type, entity_value, snapshot_date) -- prevent duplicates for the same entity and period
);

-- Drop (delete) an existing table
SELECT DISTINCT entity_type FROM trend_summary;
DROP TABLE IF EXISTS trend_summary;

-- To view aggregates_trend table

DELETE
FROM aggregates_trend
WHERE source_name = 'Women''s Wear Daily';


SELECT id,
       source_type,
       source_name,
       title,
       content,
       keywords,
       link,
       published_at,
       collected_at,
       metadata
FROM public.aggregates_trend
LIMIT 1000;


SELECT COUNT(*)
FROM aggregates_trend
WHERE source_name = 'Vogue';


SELECT COUNT(*) -- Counts everything
FROM public.aggregates_trend;


SELECT DATE(published_at) as publish_date,
       COUNT(*) as article_count
FROM aggregates_trend
GROUP BY DATE(published_at)
ORDER BY publish_date DESC;


DELETE
FROM trend_summary;
