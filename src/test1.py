from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.master("local[*]").appName("ProjectPart1").getOrCreate()
)

df = spark.read.csv("1grams.csv", sep = "\t", header = True)

df.show(5)

df.groupBy(df["#"].contains("DATABASE"))

spark.stop()