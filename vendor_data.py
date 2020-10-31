import os

from pyspark.sql import functions as F
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql import SparkSession

stream_name = 'vendorstream2'
pathOut = "s3://vendor-data-v2/data"
checkpointPath = "s3://vendor-data-resources/checkpoints/{}".format(stream_name)

spark = SparkSession \
    .builder \
    .appName("test kinesis") \
    .getOrCreate()

data_schema = StructType([
            StructField("user", StringType()),
            StructField("address", StringType()),
            StructField("time", TimestampType()),
            StructField("item", StringType()),
            StructField("price", FloatType())])

def extract_data(spark, stream_name, schema):
    # todo use LATEST startingposition
    return spark \
        .readStream \
        .format('kinesis') \
        .option('streamName', stream_name) \
        .option('endpointUrl', 'https://kinesis.us-east-1.amazonaws.com')\
        .option('region', 'us-east-1') \
        .option('startingposition', 'TRIM_HORIZON')\
        .load()\
        .selectExpr('CAST(data AS STRING)')\
        .select(F.from_json('data', schema).alias('data'))\
        .select('data.*')

def transform_data(df):
    return df.withColumn("date", F.to_date(F.col("time")))

def load_data(df, pathOut, checkpointPath):
    df.writeStream\
        .format("parquet")\
        .partitionBy("date")\
        .option("checkpointLocation", checkpointPath)\
        .option("path", pathOut)\
        .trigger(once=True)\
        .start()\
        .awaitTermination()

# excecute etl pipeline
df = extract_data(spark, stream_name, data_schema)
df_trans = transform_data(df)
load_data(df_trans, pathOut, checkpointPath)

