from pyspark.sql import SparkSession
from database import MYSQL_URL, MYSQL_PROPERTIES

spark = (
    SparkSession.builder
    .appName("MySQL Test")
    .master("local[2]")
    .config(
        "spark.jars.packages",
        "com.mysql:mysql-connector-j:8.4.0"
    )
    .getOrCreate()
)

data = [
    ("radio", 1950, 1000, 500, 100),
    ("television", 1950, 2000, 900, 200)
]

df = spark.createDataFrame(
    data,
    ["ngram", "year", "match_count", "page_count", "volume_count"]
)

df.write.jdbc(
    url=MYSQL_URL,
    table="word_year_stats",
    mode="append",
    properties=MYSQL_PROPERTIES
)

spark.stop()