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

**3. Print Data**
+ Enter MySQL:
    + `$(brew --prefix mysql@8.4)/bin/mysql -u root`
+ Use ngram database:
    + `USE ngram_db;`
+ Print Top 10 Words by Decade:
    + `SELECT * FROM decade_top_words ORDER BY decade DESC, word_rank ASC LIMIT 500;`
+ Print Top Word per Year:
    + `SELECT * FROM top_word_year ORDER BY year DESC LIMIT 20;`

Note: 'process_ngrams.py' writes word stats and top words by decade. For simplicity, only 'process_decade_top.py' and 'process_top_word_year.py' is used for Part 2.

## Website Backend (MySQL API)

The Express backend reads the processed Part 2 results from MySQL and returns JSON for the frontend charts.

The trend route reads from `word_year_stats`, which is filled by `src/process_ngrams.py`. The decade route reads from `decade_top_words`, which is filled by `src/process_decade_top.py` (or `src/process_ngrams.py`).

### Setup

1. Make sure MySQL is running and the tables in `sql/schema.sql` have been loaded.
2. Open a terminal in the `backend` folder.
3. Run `npm install`.
4. If your MySQL settings are different, copy `backend/.env.example` to `backend/.env` and edit the values. The defaults use `root`, no password, and the `ngram_db` database.
5. Run `npm start`. The API starts at `http://localhost:5000` so it does not conflict with React on port 3000.

### API Routes

- `GET /api/health` checks the MySQL connection.
- `GET /api/trends?keyword=database` returns yearly counts for a keyword.
- `GET /api/trends?keyword=database&startYear=1900&endYear=2009` optionally filters the chart years.
- `GET /api/decades` returns the available decades for a dropdown.
- `GET /api/top-words?decade=1990&limit=10` returns the most popular words for one decade.

Example frontend request:

```javascript
fetch('http://localhost:5000/api/trends?keyword=database')
  .then(response => response.json())
  .then(result => console.log(result.data));
```

## Part 3: Final Part

### How to run Web Interface

1. Open two (2) separate terminals: One in *backend* directory and the other in *frontend* directory.
2. `npm install` in both terminals
3. `npm start` in backend, then in frontend.
4. Access `http://localhost:3000/`
