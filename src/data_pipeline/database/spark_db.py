from typing import Any, Dict

from delta.tables import DeltaTable
from pyspark.sql import DataFrame, SparkSession

from .base import Database


class SparkDatabase(Database):
    def __init__(self, spark: SparkSession, catalog_config: "UnityCatalogConfig"):
        self.spark = spark
        self.catalog_config = catalog_config
    
    def read_table(self, table_name: str) -> DataFrame:
        full_table_name = f"{self.catalog_config.catalog_name}.{self.catalog_config.source_schema}.{table_name}"
        return self.spark.read.table(full_table_name)
    
    def write_table(self, df: DataFrame, table_name: str) -> None:
        full_table_name = f"{self.catalog_config.catalog_name}.{self.catalog_config.target_schema}.{table_name}"
        df.write.format("delta").mode("overwrite").saveAsTable(full_table_name)
    
    def log_operation(self, operation: Dict[str, Any]) -> None:
        log_path = self.catalog_config.log_path
        log_df = self.spark.createDataFrame([{
            "timestamp": self.spark.sql("SELECT CURRENT_TIMESTAMP").first()[0],
            "operation": operation["operation"],
            "details": str(operation["details"])
        }])
        
        log_df.write.format("delta").mode("append").save(log_path)