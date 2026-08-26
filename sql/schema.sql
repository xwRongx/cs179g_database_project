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

CREATE TABLE IF NOT EXISTS decade_top_words_no_stop (
    decade INT,
    word LONGTEXT,
    total_matches BIGINT,
    word_rank INT
);

CREATE TABLE IF NOT EXISTS decade_bottom_words (
    decade INT,
    word LONGTEXT,
    total_matches BIGINT,
    word_rank INT
);

CREATE TABLE IF NOT EXISTS decade_bottom_words_dictionary (
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

CREATE TABLE IF NOT EXISTS top_word_year_no_stop (
    year BIGINT,
    word LONGTEXT,
    total_matches BIGINT
);

CREATE TABLE IF NOT EXISTS bottom_word_year (
    year BIGINT,
    word LONGTEXT,
    total_matches BIGINT
);

CREATE TABLE IF NOT EXISTS bottom_word_year_dictionary (
    year BIGINT,
    word LONGTEXT,
    total_matches BIGINT
);

CREATE TABLE IF NOT EXISTS word_trend (
    word LONGTEXT,
    year BIGINT,
    match_count BIGINT
);