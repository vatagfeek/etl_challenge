import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
 
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
 
sparkContext = SparkContext()
glueContext = GlueContext(sparkContext)
sparkSession = glueContext.spark_session
 
 
 connection_postgres_options = {
    "url": "jdbc:mysql://<jdbc-host-name>:3306/db",
    "dbtable": "updated_salaries",
    "user": "rhoroshko",
    "password": "test"}
    
 

employee_df = sparkSession.read.format("jdbc").option("url","jdbc:postgresql:RTK=5246...;User=rhoroshko;Password=test;Database=postgres1;Server=127.0.0.1;Port=5432;")
.option("dbtable","employee").option("driver","cdata.jdbc.postgresql.PostgreSQLDriver").load()

department_df = sparkSession.read.format("jdbc").option("url","jdbc:postgresql:RTK=5246...;User=rhoroshko;Password=test;Database=postgres1;Server=127.0.0.1;Port=5432;")
.option("dbtable","employee").option("driver","cdata.jdbc.postgresql.PostgreSQLDriver").load()
 
glueJob = Job(glueContext)
glueJob.init(args['JOB_NAME'], args)
 
employee_df = employee_df.withColumnRenamed("id", "employee id")
df_joined = employee_df.join(department_df,
                               (employee_df["department id"] == department_df["id"]),
                               how="left")
 
df_joined = df_joined.withColumn("updated_salary", df_joined["salary"] * df_joined["salary_increment"]) 
df_joined = df_joined.select(["employee id", "updated_salary"])


dynamic_dframe = DynamicFrame.fromDF(df_joined, glueContext, "dynamic_df")
glueContext.write_from_options(frame_or_dfc=dynamic_dframe, connection_type="postgres",
                               connection_options=connection_postgres_options)


glueJob.commit()




