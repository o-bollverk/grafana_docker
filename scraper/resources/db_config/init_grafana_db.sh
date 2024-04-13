
# Check if DATABASE_NAME is set and its value is "desired_value"
if [ $IS_GRAFANA_DB = 1 ]; then
    psql -v ON_ERROR_STOP=1 --username $POSTGRES_USER --dbname $POSTGRES_DB <<-EOSQL

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

EOSQL
else
    echo "DATABASE_NAME is not set to the desired value. Exiting script without executing SQL commands."
fi


