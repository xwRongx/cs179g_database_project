from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("MySQL Test")
    .master("local[2]")
    .config(
        "spark.jars.packages",
        "com.mysql:mysql-connector-j:8.4.0"
    )
    .config(
        "spark.sql.legacy.charVarcharAsString",
        "true"
    )
    .getOrCreate()
)

data = [
    ("radio", 1950, 1000, 500, 100),
    ("television", 1950, 2000, 900, 200)
]

df = spark.createDataFrame(
    data,
    ["word", "year", "match_count", "page_count", "volume_count"]
)

df.printSchema()
print(df.columns)

df.write.jdbc(
    url="jdbc:mysql://127.0.0.1:3306/ngram_db",
    table="word_year_stats",
    mode="overwrite",
    properties={
        "user": "root",
        "password": "",
        "driver": "com.mysql.cj.jdbc.Driver"
    }
)

spark.stop()