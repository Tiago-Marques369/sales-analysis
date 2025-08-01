import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, desc
from dotenv import load_dotenv

# Loading variables from .env
load_dotenv()

# Initializating Spark
spark = SparkSession.builder \
    .appName("Sales Analysis") \
    .getOrCreate()

# Variables of Input Path (Local) and Output Path to S3
INPUT_PATH = "data/raw/sales_data.csv"
OUTPUT_PATH = os.getenv("S3_PATH", "output/processed/")

# CSV Reading
df = spark.read.option("header", True).option("inferSchema", True).csv(INPUT_PATH)

# Basic Cleaning
df_clean = df.dropna(subset=["order_id", "product", "quantity", "price"])
df_clean = df_clean.withColumn("quantity", col("quantity").cast("int"))
df_clean = df_clean.withColumn("price", col("price").cast("double"))
df_clean = df_clean.withColumn("total", col("quantity") * col("price"))

# Aggregated Metrics
revenue_by_category = df_clean.groupBy("category").agg(_sum("total").alias("total_revenue"))
top_products = df_clean.groupBy("product").agg(_sum("total").alias("product_revenue")).orderBy(desc("product_revenue")).limit(10)
ticket_medio = df_clean.groupBy("order_id").agg(_sum("total").alias("order_total")).agg(avg("order_total").alias("avg_ticket"))

# Writing the result on OUTPUT PATH
revenue_by_category.write.mode("overwrite").parquet(f"{OUTPUT_PATH}/revenue_by_category")
top_products.write.mode("overwrite").parquet(f"{OUTPUT_PATH}/top_products")
ticket_medio.write.mode("overwrite").parquet(f"{OUTPUT_PATH}/avg_ticket")

spark.stop()