import os
from pathlib import Path

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

from data_pipeline.config import AppConfig
from data_pipeline.database import DuckDBDatabase


@pytest.fixture(scope="session")
def spark():
    return (SparkSession.builder
            .appName("test")
            .master("local[*]")
            .getOrCreate())


@pytest.fixture(scope="session")
def test_config_path():
    """Get path to test configuration file."""
    tests_dir = Path(__file__).parent
    return tests_dir / "test_config.yml"


@pytest.fixture(scope="function")
def test_config(test_config_path):
    """Create test configuration from test YAML file."""
    return AppConfig.from_yaml(test_config_path)


@pytest.fixture(scope="session")
def sample_schema():
    return StructType([
        StructField("id", StringType(), True),
        StructField("amount", IntegerType(), True),
        StructField("category", StringType(), True)
    ])


@pytest.fixture(scope="function")
def sample_data(spark, sample_schema):
    data = [
        ("1", 100, "A"),
        ("2", 200, "B"),
        ("3", None, "C")
    ]
    return spark.createDataFrame(data, sample_schema)


@pytest.fixture(scope="function")
def test_database(spark):
    """Create a fresh DuckDB instance for each test."""
    return DuckDBDatabase(":memory:", spark)


@pytest.fixture(scope="function")
def test_pipeline(test_config, test_database):
    """Create a test pipeline instance with test configuration and database."""
    from data_pipeline.pipeline import DataPipeline
    return DataPipeline(test_config, test_database)