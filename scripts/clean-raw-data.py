import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# MC: can read the database and table names in the job parameters

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1697909563554 = glueContext.create_dynamic_frame.from_catalog(
    database="ref-pipeline-database",
    table_name="raw",
    transformation_ctx="AWSGlueDataCatalog_node1697909563554",
)

# MC: can read the queries in the job parameters (at least the name of the file containing the queries)

# Script generated for node SQL Query
SqlQuery0 = """
select *, int(Quantity) q
from raw
where order is not null
and int(Quantity) is not null

"""
SQLQuery_node1697909584940 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={"raw": AWSGlueDataCatalog_node1697909563554},
    transformation_ctx="SQLQuery_node1697909584940",
)

# MC: can read the output path and table name in the job parameters

# Script generated for node Amazon S3
AmazonS3_node1697909609017 = glueContext.getSink(
    path="s3://ref-pipeline-data-bucket-lazgar/clean/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=["date"],
    compression="gzip",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1697909609017",
)
AmazonS3_node1697909609017.setCatalogInfo(
    catalogDatabase="ref-pipeline-database", catalogTableName="clean"
)
AmazonS3_node1697909609017.setFormat("glueparquet")
AmazonS3_node1697909609017.writeFrame(SQLQuery_node1697909584940)
job.commit()
