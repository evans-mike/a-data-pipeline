from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pyspark.sql import DataFrame


class Database(ABC):
    @abstractmethod
    def read_table(self, table_name: str) -> DataFrame:
        pass
    
    @abstractmethod
    def write_table(self, df: DataFrame, table_name: str) -> None:
        pass
    
    @abstractmethod
    def log_operation(self, operation: Dict[str, Any]) -> None:
        pass