from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from database import write_bottom_word_year


# Start Spark
spark = (
    SparkSession.builder
    .appName("Least Popular Word Per Year")
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


# Rank words within each year
#
# Lowest match_count gets rank 1.
# If multiple words have the same match_count,
# alphabetical order is used as the tie-breaker.
ranking_window = (
    Window
    .partitionBy("year")
    .orderBy(
        F.asc("match_count"),
        F.asc("word")
    )
)


ranked_df = (
    df
    .withColumn(
        "word_rank",
        F.row_number().over(ranking_window)
    )
)


# Keep only the least popular word for each year
bottom_word_year_df = (
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
print("Least popular word for each year:")

bottom_word_year_df.show(
    100,
    truncate=False
)

print("Number of result rows:")
print(bottom_word_year_df.count())

print("Schema:")
bottom_word_year_df.printSchema()


# Write result into MySQL
print("Writing bottom_word_year to MySQL...")

write_bottom_word_year(bottom_word_year_df)

print("Database write complete.")


spark.stop()