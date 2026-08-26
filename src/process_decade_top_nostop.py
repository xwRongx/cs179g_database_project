from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.ml.feature import StopWordsRemover

from database import write_decade_top_words_no_stop


# Start Spark
spark = (
    SparkSession.builder
    .appName("Top Words by Decade - No Stop Words")
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
clean_df = (
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
    clean_df
    .filter(
        ~F.lower(F.col("word")).isin(stop_words)
    )
)


# Convert year into decade
# Example: 1954 -> 1950
with_decade_df = no_stop_df.withColumn(
    "decade",
    (F.floor(F.col("year") / 10) * 10).cast("int")
)


# Add total number of matches for each word within each decade
decade_totals_df = (
    with_decade_df
    .groupBy("decade", "word")
    .agg(
        F.sum("match_count").alias("total_matches")
    )
)


# Rank words separately within each decade
ranking_window = (
    Window
    .partitionBy("decade")
    .orderBy(F.desc("total_matches"))
)


ranked_df = (
    decade_totals_df
    .withColumn(
        "word_rank",
        F.row_number().over(ranking_window)
    )
)


# Keep only the top 10 words in each decade
decade_top_words_no_stop_df = (
    ranked_df
    .filter(F.col("word_rank") <= 10)
    .orderBy(
        F.desc("decade"),
        F.asc("word_rank")
    )
)


# Show results
print("Top 10 words by decade (stop words removed):")
decade_top_words_no_stop_df.show(500, truncate=False)

print("Schema:")
decade_top_words_no_stop_df.printSchema()

print("Number of rows:")
print(decade_top_words_no_stop_df.count())


# Write results to MySQL
print("Writing decade_top_words_no_stop to MySQL...")

write_decade_top_words_no_stop(decade_top_words_no_stop_df)

print("Database write complete.")


spark.stop()
