#directory per day vs directory per year demo with delta lake and apache spark

#imports-----------
import os, time
from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession, functions as F

#paths, constants------------
SRC = "demo/data/parquet/by_year"      
BY_DAY = "demo/data/delta/by_day"
BY_YEAR = "demo/data/delta/by_year"
DAY = "2025-06-07"
Y0, Y1 = 2023, 2025

#building a spark session with delta lake support--------
builder = (SparkSession.builder.master("local[4]").appName("demo")
           .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") # registers Delta's SQL parser extensions
           .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") # tells Spark's default catalog to resolve tables via Delta's catalog implementation
           .config("spark.ui.showConsoleProgress", "false")) # removes progress bar
spark = configure_spark_with_delta_pip(builder).getOrCreate() # adds the correct Delta Lake JARs to the Spark session builder
spark.sparkContext.setLogLevel("ERROR")

spark.conf.set("spark.databricks.delta.stats.skipping", "false") # disables extra stats-based skipping to reflect partition pruning alone

#write the two Delta tables----------------
for path, col in [(BY_DAY, "date"), (BY_YEAR, "year")]:
    if not os.path.exists(path):
        spark.read.parquet(SRC).repartition(col).write.format("delta").partitionBy(col).save(path)

#4 benchmark cases-----------------------
cases = [
    ("day",  "1 day",   BY_DAY,  F.col("date") == DAY),
    ("year", "1 day",   BY_YEAR, F.col("date") == DAY),
    ("day",  "3 years", BY_DAY,  F.col("year").between(Y0, Y1)),
    ("year", "3 years", BY_YEAR, F.col("year").between(Y0, Y1)),
]


def run(query, path, condition): 
    #open the table, filter, query. Returns the filtered table and the seconds it took
    t = time.perf_counter()
    f = spark.read.format("delta").load(path).filter(condition)
    q = f.select("ths200d0") if query == "1 day" else f.agg(F.avg("ths200d0"))
    q.write.format("noop").mode("overwrite").save() # write to the "noop" sink: forces full execution of the query
    return f, time.perf_counter() - t

#warm-up--------------------------------------------
#to avoid JIT/compiling overhead
for _ in range(3):
    for layout, query, path, condition in cases:
        run(query, path, condition)

#timed runs--------------------------------------
#Each case runs 5 times and the median is reported
print(f"\n{'layout':<7}{'query':<9}{'seconds':>9}{'files':>8}")
for layout, query, path, condition in cases:
    times = []
    for _ in range(5):
        f, secs = run(query, path, condition)
        times.append(secs)
    files = f.select(F.input_file_name()).distinct().count()   # files that survive the pruning
    print(f"{layout:<7}{query:<9}{sorted(times)[2]:>9.2f}{files:>8}")

spark.stop()