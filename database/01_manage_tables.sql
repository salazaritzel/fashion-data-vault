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