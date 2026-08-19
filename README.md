# cs179g_database_project
Description: Database project using google n-grams dataset to analyze word trends.

## Useful Terminal Commands

Install requirements.txt:\
`cd cs179g_database_project`\
`python -m pip install -r requirements.txt`

Access MySQL:\
`$(brew --prefix mysql@8.4)/bin/mysql -u root`\
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

## Part 2: Store Top 10 Words (By Decade) to MySQL Database
1. Load 'clean_ngram.csv' into 'data' folder.

2. Load schema onto local MySQL database.
+ `$(brew --prefix mysql@8.4)/bin/mysql -u root < sql/schema.sql` (Mac-based, change according to device)\
+ `python src/process_decade_top.py`

3. Print Top 10 Words by the Decade
+ `$(brew --prefix mysql@8.4)/bin/mysql -u root` (Enter MySQL)
+ `USE ngram_db;`
+ `SELECT COUNT(*) FROM decade_top_words;`
+ `SELECT * FROM decade_top_words ORDER BY decade, word_rank LIMIT 500;`