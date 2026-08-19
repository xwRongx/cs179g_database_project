# CS179G Database Project (Group 3)
Description: Database project using google n-grams dataset to analyze word trends.

## Useful Terminal Commands

Install requirements.txt:\
`cd cs179g_database_project`\
`python -m pip install -r requirements.txt`

Access MySQL:\
`$(brew --prefix mysql@8.4)/bin/mysql -u root`

Run Schema in MySQL:\
`$(brew --prefix mysql@8.4)/bin/mysql -u root < sql/schema.sql`

MySQL:\
`SHOW DATABASES;`\
`USE ngram_db;`\
`SHOW TABLES;`\
`DESCRIBE word_year_stats;`\
`SELECT * FROM word_year_stats;`\
`exit;`

PySpark:\
`python src/tests/test3_mysql.py`\
`python src/process_ngrams.py`

## Part 2: Top 10 Words (per Decade) & Top Word (per Year)
**1. Load 'clean_ngram.csv' into 'data' folder.**

**2. Load schema onto local MySQL database.**
+ `$(brew --prefix mysql@8.4)/bin/mysql -u root < sql/schema.sql` 
    + Mac-based, change according to device
+ `python src/process_decade_top.py`
    + Sorts 'clean_ngram.csv' and writes "Top 10 Words per Decade"
+ `python src/process_top_word_year.py`
    + Sorts 'clean_ngram.csv' and writes "Top Word per Year"

**3. Print Top 10 Words by the Decade (1580-2000)**
+ Enter MySQL:
    + `$(brew --prefix mysql@8.4)/bin/mysql -u root`
+ Use ngram database:
    + `USE ngram_db;`
+ Print Top 10 Words by Decade:
    + `SELECT * FROM decade_top_words ORDER BY decade DESC, word_rank ASC LIMIT 500;`
+ Print Top Word per Year:
    + `SELECT * FROM top_word_year ORDER BY year DESC LIMIT 20;`

Note: 'process_ngrams.py' writes word stats and top words by decade. For simplicity, only 'process_decade_top.py' is used for Part 2.