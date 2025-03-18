import pytest
from pyspark.sql import DataFrame

from data_pipeline.pipeline import DataPipeline


class TestPipelineIntegration:
    """Integration tests for the complete pipeline."""

    def test_pipeline_end_to_end(self, test_pipeline, test_database, sample_data):
        """Test the complete pipeline flow from source to target."""
        # Set up
        source_table = "source_data"
        target_table = "target_data"
        
        # Write test data
        test_database.write_table(sample_data, source_table)
        
        # Run pipeline
        test_pipeline.run(source_table, target_table)
        
        # Verify results
        result = test_database.read_table(target_table)
        
        # Check transformations were applied
        assert "processing_ts" in result.columns
        assert "metric_value" in result.columns
        assert all(col.islower() for col in result.columns)
        
        # Check data integrity
        assert result.count() == sample_data.count()
        
        # Check specific transformations
        metrics = result.select("id", "amount", "metric_value").collect()
        for row in metrics:
            if row.amount is None:
                assert row.metric_value == 0
            else:
                assert row.metric_value == row.amount

    def test_pipeline_error_handling(self, test_pipeline):
        """Test pipeline error handling with invalid table."""
        with pytest.raises(Exception) as exc_info:
            test_pipeline.run("nonexistent_table", "target_table")
        
        # Verify error is logged
        # Note: In a real application, you might want to check the logs table
        assert "nonexistent_table" in str(exc_info.value)

    def test_pipeline_with_empty_source(self, test_pipeline, test_database, spark, sample_schema):
        """Test pipeline behavior with empty source table."""
        # Create empty DataFrame with same schema
        empty_df = spark.createDataFrame([], sample_schema)
        
        # Set up
        source_table = "empty_source"
        target_table = "empty_target"
        
        # Write empty data
        test_database.write_table(empty_df, source_table)
        
        # Run pipeline
        test_pipeline.run(source_table, target_table)
        
        # Verify results
        result = test_database.read_table(target_table)
        assert result.count() == 0
        assert all(expected_col in result.columns for expected_col in empty_df.columns)
        assert "processing_ts" in result.columns