CREATE DATABASE IF NOT EXISTS ngram_db;

USE ngram_db;

CREATE TABLE IF NOT EXISTS word_year_stats (
    ngram VARCHAR(255),
    year INT,
    match_count BIGINT,
    page_count BIGINT,
    volume_count BIGINT,
    PRIMARY KEY (ngram, year)
);

CREATE TABLE IF NOT EXISTS decade_top_words (
    decade INT,
    ngram VARCHAR(255),
    total_matches BIGINT,
    word_rank INT
);