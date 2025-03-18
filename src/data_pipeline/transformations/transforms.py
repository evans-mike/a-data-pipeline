from typing import Callable

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def add_processing_timestamp(df: DataFrame) -> DataFrame:
    """Add processing timestamp to the DataFrame."""
    return df.withColumn("processing_ts", F.current_timestamp())


def clean_column_names(df: DataFrame) -> DataFrame:
    """Convert column names to snake_case."""
    for col in df.columns:
        clean_name = col.lower().replace(" ", "_")
        df = df.withColumnRenamed(col, clean_name)
    return df


def calculate_metrics(df: DataFrame) -> DataFrame:
    """Calculate example metrics."""
    return df.withColumn(
        "metric_value",
        F.when(F.col("amount").isNotNull(), F.col("amount"))
         .otherwise(0)
    )


# Function composition helper
def compose(*functions: Callable) -> Callable:
    def compose_two(f: Callable, g: Callable) -> Callable:
        return lambda x: f(g(x))
    
    return reduce(compose_two, functions)


# Create pipeline transformation combining all transforms
transform_pipeline = compose(
    calculate_metrics,
    clean_column_names,
    add_processing_timestamp
)