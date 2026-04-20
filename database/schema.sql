-- This table is where I display all my different data sources.

CREATE TABLE IF NOT EXISTS data_sources (id SERIAL PRIMARY KEY,
                                                   name VARCHAR(100) NOT NULL,
                                                                     type VARCHAR(50) NOT NULL,
                                                                                      url VARCHAR(500),
                                                                                          is_active BOOLEAN DEFAULT true,
                                                                                                                    created_at TIMESTAMP DEFAULT NOW());

-- This is where I will be storing articles, relevant to what is being analyzed

CREATE TABLE IF NOT EXISTS articles (id SERIAL PRIMARY KEY,
                                               source_id INTEGER REFERENCES data_sources(id),
                                                                            title TEXT NOT NULL,
                                                                                       content TEXT, author VARCHAR(255),
                                                                                                            published_at TIMESTAMP, url VARCHAR(500),
                                                                                                                                        created_at TIMESTAMP DEFAULT NOW());

-- To view data_sources table

SELECT id,
       name,
       type,
       url,
       is_active,
       created_at
FROM public.data_sources
LIMIT 1000;


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

-- For auditing purposes: Table for logging what the adapters are doing.

CREATE TABLE IF NOT EXISTS audit_log (id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                                                                  adapter_name TEXT NOT NULL, -- Which adapter file ran
 status TEXT NOT NULL, -- "Success" or "Error"
 message TEXT, -- Details or error info
 logged_at TIMESTAMP NOT NULL DEFAULT NOW());

-- To view audit_log table

SELECT id,
       adapter_name,
       status,
       message,
       logged_at
FROM public.audit_log
LIMIT 1000;


SELECT source_name,
       COUNT(*) as article_count
FROM aggregates_trend
GROUP BY source_name
ORDER BY article_count DESC;


SELECT source_name,
       MIN(published_at) as earliest,
       MAX(published_at) as latest
FROM aggregates_trend
WHERE published_at IS NOT NULL
GROUP BY source_name;


SELECT source_name,
       title
FROM aggregates_trend
ORDER BY published_at DESC
LIMIT 50;


SELECT source_name,
       DATE_PART('year', published_at) as year,
       COUNT(*) as count
FROM aggregates_trend
GROUP BY source_name,
         year
ORDER BY source_name,
         year DESC;


SELECT source_name,
       COUNT(*) as old_articles
FROM aggregates_trend
WHERE published_at < NOW() - INTERVAL '90 days'
GROUP BY source_name
ORDER BY old_articles DESC;


SELECT COUNT(*) -- Counts everything
FROM public.aggregates_trend;


SELECT DATE(published_at) as publish_date,
       COUNT(*) as article_count
FROM aggregates_trend
GROUP BY DATE(published_at)
ORDER BY publish_date DESC;


DELETE
FROM trend_summary;


SELECT snapshot_date,
       COUNT(*) as entries
FROM trend_summary
GROUP BY snapshot_date
ORDER BY snapshot_date DESC
LIMIT 10;


SELECT SUM(count) as total_mentions,
       COUNT(DISTINCT snapshot_date) as days_mentioned,
       MIN(snapshot_date) as first_mention,
       MAX(snapshot_date) as last_mention
FROM public.trend_summary
WHERE entity_type = 'material'
    AND entity_value = 'cotton'
    AND snapshot_date >= '2025-11-01';


SELECT title, source_name, link, COUNT(*) as count
FROM aggregates_trend
WHERE title = 'at the cfda awards, recession beauty hacks get real'
GROUP BY title, source_name, link;