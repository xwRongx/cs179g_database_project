from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Ngram Processing")
    .master("local[2]")
    .config(
        "spark.jars.packages",
        "com.mysql:mysql-connector-j:8.4.0"
    )
    .getOrCreate()
)