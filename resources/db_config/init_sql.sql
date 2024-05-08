CREATE SCHEMA IF NOT EXISTS scraping_analysis; 

CREATE TABLE IF NOT EXISTS scraping_analysis.hourly_keyword_counts (
    term VARCHAR(255),
    incidence INTEGER,
    site VARCHAR(255),
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scraping_analysis.hourly_keyword_counts_test (
    term VARCHAR(255),
    incidence INTEGER,
    site VARCHAR(255),
    timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scraping_analysis.sentiment_scores (
    term VARCHAR(255),
    average_sentiment INTEGER,
    site VARCHAR(255),
    timestamp TIMESTAMP
);

CREATE USER grafanareader WITH PASSWORD 'password';
GRANT USAGE ON SCHEMA scraping_analysis TO grafanareader;
GRANT SELECT ON scraping_analysis.hourly_keyword_counts TO grafanareader;
GRANT SELECT ON scraping_analysis.sentiment_scores TO grafanareader;

ALTER ROLE grafanareader SET search_path = 'scraping_analysis';

-- Add default data to the database
COPY scraping_analysis.hourly_keyword_counts(term, incidence, site, timestamp) FROM '/opt/dev/sample_data/init_csv/sample_csv_theguardian.csv' DELIMITER ',' CSV HEADER;

