from pyspark.sql import SparkSession
import argparse

def main():
    parser = argparse.ArgumentParser(description="View ETL output with PySpark")
    parser.add_argument("--path", required=True, help="Path to output folder (local)")
    args = parser.parse_args()

    spark = SparkSession.builder.appName("ViewOutput").getOrCreate()

    print(f"\nReading from: {args.path}")
    df = spark.read.parquet(args.path)
    df.show(20, truncate=False)
    df.printSchema()

    spark.stop()


if __name__ == "__main__":
    main()
