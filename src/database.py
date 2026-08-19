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

# Writes the Spark DataFrame containing the top words for each decade into the decade_top_words MySQL table.
def write_decade_top_words(df):
    df.write.jdbc(
        url=MYSQL_URL,
        table="decade_top_words",
        mode="overwrite",
        properties=MYSQL_PROPERTIES
    )