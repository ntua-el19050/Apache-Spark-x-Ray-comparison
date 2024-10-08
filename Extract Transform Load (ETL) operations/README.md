# How to run the ETL operations
--------------------------------------------------------------

With these scripts we perform some simple ETL operations on our data in order to compare the results between Ray and Spark.

### Aggregate Filter
In aggregate and filter we select 3 of the columns, then filter them based on a value of one of the columns and from the filtered dataframe we add the average trip_time on a different time, grouped based on PULocationID.

### Sort
In sort we simply sort our data.

### Transform
In transform we transform one column of our data and add the results in a new one

## Spark runs

If you want to run all of them for one set of years for 2 and 3 workers run the code below:
```bash
./runSparkETL
```

For individual runs you can run it with the following line:
```bash
spark-submit --conf spark.log.level=WARN --conf spark.executorEnv.PYSPARK_PYTHON=/usr/bin/python3 --packages ch.cern.sparkmeasure:spark-measure_2.12:0.24 aggregateFilterSpark.py {num_workers=2,3}
spark-submit --conf spark.log.level=WARN --conf spark.executorEnv.PYSPARK_PYTHON=/usr/bin/python3 --packages ch.cern.sparkmeasure:spark-measure_2.12:0.24 sortSpark.py {num_workers=2,3}
spark-submit --conf spark.log.level=WARN --conf spark.executorEnv.PYSPARK_PYTHON=/usr/bin/python3 --packages ch.cern.sparkmeasure:spark-measure_2.12:0.24 transformSpark.py {num_workers=2,3}
```

Unfortunately in order to change the set of years it reads data from you need to edit the code of each one of them.

## Ray runs

For runs for all years but for 2 or 3 workers only, according to the configuration of your cluster, you can run the following line of code:
```bash
./runRayETL
```

If you want individual runs, you need the following line of code:
```bash
python3 aggregateFilterRay.py {num_years=1,2,3}
python3 sortRay.py {num_years=1,2,3}
python3 transformRay.py {num_years=1,2,3}
```