MYSQL_URL = "jdbc:mysql://127.0.0.1:3306/ngram_db"

MYSQL_PROPERTIES = {
    "user": "root",
    "password": "",
    "driver": "com.mysql.cj.jdbc.Driver"
}

# Writes the Spark DataFrame containing yearly word statistics into the word_year_stats MySQL table.
def write_word_year_stats(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="word_year_stats",
        mode="overwrite", # Changed from "append" to "overwrite" due to PySpark version compatibility
        properties=MYSQL_PROPERTIES
    )

# Writes the Spark DataFrame containing the top words for each decade into decade_top_words MySQL table.
def write_decade_top_words(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="decade_top_words",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )

# Writes the top words for each decade with stop words removed.
def write_decade_top_words_no_stop(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="decade_top_words_no_stop",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )

# Writes the Spark DataFrame containing the bottom words for each decade into decade_bottom_words MySQL table.
def write_decade_bottom_words(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="decade_bottom_words",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )

# Writes the bottom dictionary words for each decade.
def write_decade_bottom_words_dictionary(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="decade_bottom_words_dictionary",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )

# Writes the Spark DataFrame containing the top word per year into top_word_year MySQL table.
def write_top_word_year(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="top_word_year",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )

# Writes the top word per year with stop words removed.
def write_top_word_year_no_stop(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="top_word_year_no_stop",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )

# Writes the Spark DataFrame containing the bottom word per year into bottom_word_year MySQL table.
def write_bottom_word_year(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="bottom_word_year",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )

# Writes the bottom dictionary word per year.
def write_bottom_word_year_dictionary(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="bottom_word_year_dictionary",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )

# Writes the Spark DataFrame containing a specified word and its trends per year into word_trend MySQL table.
def write_word_trend(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="word_trend",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )