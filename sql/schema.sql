CREATE DATABASE IF NOT EXISTS ngram_db;

USE ngram_db;


CREATE TABLE IF NOT EXISTS word_year_stats (
    word LONGTEXT,
    year BIGINT,
    match_count BIGINT,
    page_count BIGINT,
    volume_count BIGINT
);


CREATE TABLE IF NOT EXISTS decade_top_words (
    decade INT,
    word LONGTEXT,
    total_matches BIGINT,
    word_rank INT
);


CREATE TABLE IF NOT EXISTS top_word_year (
    year BIGINT,
    word LONGTEXT,
    total_matches BIGINT
);


CREATE TABLE IF NOT EXISTS word_trend (
    word LONGTEXT,
    year BIGINT,
    match_count BIGINT
);