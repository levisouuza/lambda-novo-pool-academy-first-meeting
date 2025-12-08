import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(
    sys.argv, [
        'JOB_NAME',
        "FILE_PATH"
        ]
    )

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

options = {
    "header": "true",
    "inferSchema": "true",
}

df = spark.read.format("csv").options(**options).load(args["FILE_PATH"])
df.show(truncate=False)

job.commit()
