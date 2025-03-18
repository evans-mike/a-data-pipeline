import pytest
from pyspark.sql import DataFrame

from data_pipeline.pipeline import DataPipeline


def test_pipeline_end_to_end(test_config, test_database, sample_data):
    # Set up
    pipeline = DataPipeline(test_config, test_database)
    source_table = "source_data"
    target_table = "target_data"
    
    # Write test data
    test_database.write_table(sample_data, source_table)
    
    # Run pipeline
    pipeline.run(source_table, target_table)
    
    # Verify results
    result = test_database.read_table(target_table)
    
    # Check transformations were applied
    assert "processing_ts" in result.columns
    assert "metric_value" in result.columns
    assert all(col.islower() for col in result.columns)
    
    # Check data integrity
    assert result.count() == sample_data.count()


def test_pipeline_error_handling(test_config, test_database):
    pipeline = DataPipeline(test_config, test_database)
    
    with pytest.raises(Exception):
        pipeline.run("nonexistent_table", "target_table")