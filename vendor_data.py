from pyspark.sql.functions import *
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql import SparkSession

stream_name = 'vendorstream2'

spark = SparkSession \
    .builder \
    .appName("test kinesis") \
    .getOrCreate()

# todo use LATEST
kinesis = spark \
        .readStream \
        .format('kinesis') \
        .option('streamName', stream_name) \
        .option('endpointUrl', 'https://kinesis.us-east-1.amazonaws.com')\
        .option('region', 'us-east-1') \
        .option('awsAccessKeyId', os.environ['AWS_ACCESS_KEY_ID'])\
        .option('awsSecretKey', os.environ['AWS_SECRET_ACCESS_KEY']) \
        .option('startingposition', 'TRIM_HORIZON')\
        .load()\

schema = StructType([
            StructField("message_type", StringType()),
            StructField("count", IntegerType())])
kinesis\
    .selectExpr('CAST(data AS STRING)')\
    .select(from_json('data', schema).alias('data'))\
    .select('data.*')\
    .writeStream\
    .outputMode('append')\
    .format('console')\
    .trigger(once=True) \
    .start()\
    .awaitTermination()

