import argparse
import os
from pyspark.sql import SparkSession
from dotenv import load_dotenv

def main():
    load_dotenv()  # Loading .env variables

    parser = argparse.ArgumentParser(description="View parquet output with PySpark")
    parser.add_argument('--path', type=str, required=True, help='Path to parquet files (local or s3a)')
    args = parser.parse_args()

    spark = (
        SparkSession.builder
        .appName("ViewOutput")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
        .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
        .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com")
        .getOrCreate()
    )

    df = spark.read.parquet(args.path)
    df.show(truncate=False)

    spark.stop()

if __name__ == "__main__":
    main()
