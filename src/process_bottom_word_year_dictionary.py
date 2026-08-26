from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from database import write_bottom_word_year_dictionary


# Start Spark
spark = (
    SparkSession.builder
    .appName("Least Popular Dictionary Word Per Year")
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
    df
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


# Rank words within each year
# Lowest match_count receives rank 1
# Alphabetical order breaks ties
ranking_window = (
    Window
    .partitionBy("year")
    .orderBy(
        F.asc("match_count"),
        F.asc("normalized_word")
    )
)


ranked_df = (
    dictionary_words_df
    .withColumn(
        "word_rank",
        F.row_number().over(ranking_window)
    )
)


# Keep only the least popular dictionary word for each year
bottom_word_year_dictionary_df = (
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
print("Least popular dictionary word for each year:")

bottom_word_year_dictionary_df.show(
    100,
    truncate=False
)

print("Number of result rows:")
print(bottom_word_year_dictionary_df.count())

print("Schema:")
bottom_word_year_dictionary_df.printSchema()


# Write result into MySQL
print("Writing bottom_word_year_dictionary to MySQL...")

write_bottom_word_year_dictionary(bottom_word_year_dictionary_df)

print("Database write complete.")


spark.stop()
