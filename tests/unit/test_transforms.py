import pytest
from pyspark.sql import DataFrame

from data_pipeline.transformations import transforms


def test_add_processing_timestamp(sample_data):
    result = transforms.add_processing_timestamp(sample_data)
    assert "processing_ts" in result.columns


def test_clean_column_names(spark):
    data = [("1", 100)]
    df = spark.createDataFrame(data, ["ID Number", "Amount Value"])
    
    result = transforms.clean_column_names(df)
    assert all(col in result.columns for col in ["id_number", "amount_value"])


def test_calculate_metrics(sample_data):
    result = transforms.calculate_metrics(sample_data)
    
    # Check null amounts are converted to 0
    null_metrics = result.filter("amount IS NULL").collect()
    assert all(row.metric_value == 0 for row in null_metrics)
    
    # Check non-null amounts are preserved
    valid_metrics = result.filter("amount IS NOT NULL").collect()
    assert all(row.metric_value == row.amount for row in valid_metrics)


def test_transform_pipeline(sample_data):
    result = transforms.transform_pipeline(sample_data)
    
    assert "processing_ts" in result.columns
    assert all(col.islower() for col in result.columns)
    assert "metric_value" in result.columns