from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.master("local[*]").appName("ProjectPart1").getOrCreate()
)

df = spark.read.csv("test.csv", header = True)

df.show()

df.createOrReplaceTempView("people")

query = spark.sql(""" SELECT COUNT(*) AS people78727 FROM people WHERE zipcode = 78727 """)

query.show()

spark.stop()