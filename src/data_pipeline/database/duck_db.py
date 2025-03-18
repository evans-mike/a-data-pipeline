import duckdb
from pyspark.sql import DataFrame, SparkSession

from .base import Database


class DuckDBDatabase(Database):
    def __init__(self, path: str, spark: SparkSession):
        self.conn = duckdb.connect(path)
        self.spark = spark
    
    def read_table(self, table_name: str) -> DataFrame:
        # Convert DuckDB result to Spark DataFrame
        duck_df = self.conn.sql(f"SELECT * FROM {table_name}")
        return self.spark.createDataFrame(duck_df.to_df())
    
    def write_table(self, df: DataFrame, table_name: str) -> None:
        # Convert Spark DataFrame to DuckDB table
        pandas_df = df.toPandas()
        self.conn.register(table_name, pandas_df)
    
    def log_operation(self, operation: Dict[str, Any]) -> None:
        self.conn.sql("""
            CREATE TABLE IF NOT EXISTS pipeline_logs (
                timestamp TIMESTAMP,
                operation VARCHAR,
                details JSON
            )
        """)
        self.conn.sql(
            "INSERT INTO pipeline_logs VALUES (CURRENT_TIMESTAMP, ?, ?)",
            [operation["operation"], operation["details"]]
        )