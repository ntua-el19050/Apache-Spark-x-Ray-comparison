from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from sparkmeasure import TaskMetrics, StageMetrics
from pyspark.sql.functions import col, sum, count
import os
import sys
import time

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

def write_metrics_to_file(metrics, filename, run_id):
    with open(filename, 'a') as f:
        f.write("\nTRANSFORM, 2019 Dataset")
        f.write(f"\nRun ID: {run_id}\n")
        f.write("Stage Metrics:\n")
        for metric, value in metrics['stagemetrics'].items():
            f.write(f"{metric}: {value}\n")
        f.write("\nMemory Report:\n")
        f.write(metrics['memory_report'])
        
# Initialize Spark
spark = SparkSession \
    .builder \
    .appName("Transform") \
    .master("yarn") \
    .config("spark.executor.instances", sys.argv[1]) \
    .getOrCreate()

init_time = time.time()
stagemetrics = StageMetrics(spark)

# Read the taxi data from HDFS
print("Reading data from HDFS...")
# Add 2019 only for the 2019 files, 2019, 2020 for these 2 years and 2019, 2020, 2021 for 3 years
taxi_data = spark.read.parquet("hdfs:///taxi_drivers/{2019, 2020, 2021}/*.parquet")

stagemetrics.begin()
start_time = time.time()

# Select relevant columns and calculate the mean speed
print("Calculating Mean Speed...")
sorted_df = taxi_data.select("PULocationID", "DOLocationID", "trip_miles", "trip_time") \
    .withColumn("speed", col("trip_miles") / col("trip_time") / (60 * 60))

# Display the sorted data
print("\nTransformed Rows:")
print(sorted_df.count())

stagemetrics.end()
finish_time = time.time()

read_time = start_time - init_time
query_time = finish_time - start_time 

with open("SparkETLTimeResults.txt", 'a') as f:
    f.write("\nTRANSFORM, 2019, 2020, 2021 Dataset")
    f.write(f"\nExecutors: {sys.argv[1]}\n")
    f.write(f"Data Read Time: {read_time}\n")
    f.write(f"Query Time: {query_time}\n")
    f.write(f"==================================\n\n")
    
# Collect the stage metrics
stage_metrics = stagemetrics.aggregate_stagemetrics()

# Initialize metrics dictionary
metrics = {
    'stagemetrics': stage_metrics,
    'memory_report': ""
}

# Wait for memory report
timer = 100
while timer > 0:
    try:
        memory_report = stagemetrics.report_memory()
        metrics['memory_report'] = memory_report
        break
    except:
        print("Waiting for memory report...")
        time.sleep(5)
        timer -= 5
if not metrics['memory_report']:
    metrics['memory_report'] = ["Memory report timeout"]

# Write metrics to file
write_metrics_to_file(metrics, 'SparkETLResults.txt', sys.argv[2])