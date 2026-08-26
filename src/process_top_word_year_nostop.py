from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.ml.feature import StopWordsRemover

from database import write_top_word_year_no_stop


# Start Spark
spark = (
    SparkSession.builder
    .appName("Most Popular Word Per Year - No Stop Words")
    .master("local[2]")
    .config(
        "spark.jars.packages",
        "com.mysql:mysql-connector-j:8.4.0"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


# Load cleaned Ngram data
df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv("data/clean_ngram.csv")
)


# Basic validation
df = (
    df
    .dropna(subset=["word", "year", "match_count"])
    .filter(F.col("word") != "")
    .filter(F.col("year") > 0)
    .filter(F.col("match_count") >= 0)
)


# Load Spark's default English stop-word list
stop_words = StopWordsRemover.loadDefaultStopWords("english")


# Remove stop words
no_stop_df = (
    df
    .filter(
        ~F.lower(F.col("word")).isin(stop_words)
    )
)


# Rank words within each year by match_count
# Highest match_count receives rank 1
ranking_window = (
    Window
    .partitionBy("year")
    .orderBy(
        F.desc("match_count"),
        F.asc("word")
    )
)


ranked_df = (
    no_stop_df
    .withColumn(
        "word_rank",
        F.row_number().over(ranking_window)
    )
)


# Keep only the most popular word for each year
top_word_year_no_stop_df = (
    ranked_df
    .filter(F.col("word_rank") == 1)
    .select(
        F.col("year"),
        F.col("word"),
        F.col("match_count").alias("total_matches")
    )
    .orderBy(F.desc("year"))
)


# Display Spark results
print("Most popular word for each year (stop words removed):")

top_word_year_no_stop_df.show(
    100,
    truncate=False
)

print("Number of result rows:")
print(top_word_year_no_stop_df.count())

print("Schema:")
top_word_year_no_stop_df.printSchema()


# Write result into MySQL
print("Writing top_word_year_no_stop to MySQL...")

write_top_word_year_no_stop(top_word_year_no_stop_df)

print("Database write complete.")


spark.stop()
