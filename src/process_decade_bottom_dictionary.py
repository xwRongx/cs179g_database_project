from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from database import write_decade_bottom_words_dictionary


# Start Spark
spark = (
    SparkSession.builder
    .appName("Bottom Dictionary Words by Decade")
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
    .filter(F.col("match_count") > 0)
)


# Load English dictionary
# Expected format: one word per line
dictionary_df = (
    spark.read
    .text("data/words_alpha.txt")
    .select(
        F.lower(F.trim(F.col("value"))).alias("dictionary_word")
    )
    .filter(F.col("dictionary_word") != "")
    .dropDuplicates()
)


# Normalize Ngram words for matching
normalized_df = (
    clean_df
    .withColumn(
        "normalized_word",
        F.lower(F.trim(F.col("word")))
    )
)


# Keep only words found in the dictionary
dictionary_words_df = (
    normalized_df
    .join(
        dictionary_df,
        normalized_df.normalized_word == dictionary_df.dictionary_word,
        "inner"
    )
    .drop("dictionary_word")
)


# Convert year into decade
# Example: 1954 -> 1950
with_decade_df = dictionary_words_df.withColumn(
    "decade",
    (F.floor(F.col("year") / 10) * 10).cast("int")
)


# Add total matches for each word within each decade
decade_totals_df = (
    with_decade_df
    .groupBy("decade", "word", "normalized_word")
    .agg(
        F.sum("match_count").alias("total_matches")
    )
)


# Rank words separately within each decade
# Lowest total_matches receives rank 1
ranking_window = (
    Window
    .partitionBy("decade")
    .orderBy(
        F.asc("total_matches"),
        F.asc("normalized_word")
    )
)


ranked_df = (
    decade_totals_df
    .withColumn(
        "word_rank",
        F.row_number().over(ranking_window)
    )
)


# Keep only the bottom 10 dictionary words in each decade
decade_bottom_words_dictionary_df = (
    ranked_df
    .filter(F.col("word_rank") <= 10)
    .select(
        F.col("decade"),
        F.col("word"),
        F.col("total_matches"),
        F.col("word_rank")
    )
    .orderBy(
        F.desc("decade"),
        F.asc("word_rank")
    )
)


# Display Spark results
print("Bottom 10 dictionary words by decade:")

decade_bottom_words_dictionary_df.show(
    500,
    truncate=False
)

print("Number of result rows:")
print(decade_bottom_words_dictionary_df.count())

print("Schema:")
decade_bottom_words_dictionary_df.printSchema()


# Write result into MySQL
print("Writing decade_bottom_words_dictionary to MySQL...")

write_decade_bottom_words_dictionary(decade_bottom_words_dictionary_df)

print("Database write complete.")


spark.stop()
