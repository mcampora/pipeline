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

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1697916209651 = glueContext.create_dynamic_frame.from_catalog(
    database="ref-pipeline-database",
    table_name="clean",
    transformation_ctx="AWSGlueDataCatalog_node1697916209651",
)

# Script generated for node SQL Query
SqlQuery0 = """
select client, count(*) nb
from clean
group by client

"""
SQLQuery_node1697916218868 = sparkSqlQuery(
    glueContext,
    query=SqlQuery0,
    mapping={"clean": AWSGlueDataCatalog_node1697916209651},
    transformation_ctx="SQLQuery_node1697916218868",
)

# Script generated for node Amazon S3
AmazonS3_node1697916226458 = glueContext.getSink(
    path="s3://ref-pipeline-data-bucket-lazgar/prepared/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="gzip",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1697916226458",
)
AmazonS3_node1697916226458.setCatalogInfo(
    catalogDatabase="ref-pipeline-database", catalogTableName="prepared"
)
AmazonS3_node1697916226458.setFormat("glueparquet")
AmazonS3_node1697916226458.writeFrame(SQLQuery_node1697916218868)
job.commit()
