from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from database import write_top_word_year


# Start Spark
spark = (
    SparkSession.builder
    .appName("Most Popular Word Per Year")
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


# Create two aliases of the same DataFrame
a = df.alias("a")
b = df.alias("b")

# Find the highest match_count for each year
df2 = (
    b
    .groupBy(b.year)
    .agg(
        F.max(b.match_count).alias("highestCount")
    )
)

# Join the maximum count back to the original DataFrame
# to determine which word had that count
top_word_year_df = (
    a
    .join(
        df2,
        [
            a.year == df2.year,
            a.match_count == df2.highestCount
        ]
    )
    .select(
        a.year.alias("year"),
        a.word.alias("word"),
        df2.highestCount.alias("total_matches")
    )
    .orderBy(F.desc(a.year))
)


# Display Spark results
print("Most popular word for each year:")

top_word_year_df.show(
    100, #adjust to display more/less rows
    truncate=False
)

print("Number of result rows:")
print(top_word_year_df.count())

print("Schema:")
top_word_year_df.printSchema()


# Write result into MySQL
print("Writing top_word_year to MySQL...")

write_top_word_year(top_word_year_df)

print("Database write complete.")


spark.stop()