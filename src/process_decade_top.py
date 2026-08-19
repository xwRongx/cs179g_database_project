from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from database import write_decade_top_words


# Start Spark
spark = (
    SparkSession.builder
    .appName("Top Words by Decade")
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


# Convert year into decade
# Example: 1954 -> 1950
with_decade_df = clean_df.withColumn(
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
decade_top_words_df = (
    ranked_df
    .filter(F.col("word_rank") <= 10)
    .orderBy("decade", "word_rank")
)


# Show results
print("Top 10 words by decade:")
decade_top_words_df.show(500, truncate=False)

print("Schema:")
decade_top_words_df.printSchema()

print("Number of rows:")
print(decade_top_words_df.count())


# Write results to MySQL
print("Writing decade_top_words to MySQL...")

write_decade_top_words(decade_top_words_df)

print("Database write complete.")


spark.stop()