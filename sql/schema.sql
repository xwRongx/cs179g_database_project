CREATE DATABASE IF NOT EXISTS ngram_db;

USE ngram_db;

CREATE TABLE IF NOT EXISTS word_year_stats (
    word VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    match_count BIGINT NOT NULL,
    page_count BIGINT NOT NULL,
    volume_count BIGINT NOT NULL,
    PRIMARY KEY (word, year)
);

CREATE TABLE IF NOT EXISTS decade_top_words (
    decade INT NOT NULL,
    word VARCHAR(255) NOT NULL,
    total_matches BIGINT NOT NULL,
    word_rank INT NOT NULL,
    PRIMARY KEY (decade, word_rank)
);