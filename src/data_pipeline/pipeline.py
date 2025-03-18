from typing import Optional

from pyspark.sql import SparkSession

from .config import AppConfig
from .database import Database, DuckDBDatabase, SparkDatabase
from .transformations import transform_pipeline


class DataPipeline:
    def __init__(self, config: AppConfig, database: Optional[Database] = None):
        self.config = config
        self.spark = self._create_spark_session()
        self.database = database or self._create_database()
    
    def _create_spark_session(self) -> SparkSession:
        return (SparkSession.builder
                .appName(self.config.spark.app_name)
                .master(self.config.spark.master)
                .getOrCreate())
    
    def _create_database(self) -> Database:
        if self.config.database.type == "duckdb":
            return DuckDBDatabase(self.config.database.path, self.spark)
        return SparkDatabase(self.spark, self.config.unity_catalog)
    
    def run(self, source_table: str, target_table: str) -> None:
        try:
            # Read source data
            df = self.database.read_table(source_table)
            
            # Apply transformations
            transformed_df = transform_pipeline(df)
            
            # Write results
            self.database.write_table(transformed_df, target_table)
            
            # Log success
            self.database.log_operation({
                "operation": "pipeline_run",
                "details": {
                    "source": source_table,
                    "target": target_table,
                    "status": "success"
                }
            })
            
        except Exception as e:
            # Log failure
            self.database.log_operation({
                "operation": "pipeline_run",
                "details": {
                    "source": source_table,
                    "target": target_table,
                    "status": "failed",
                    "error": str(e)
                }
            })
            raise