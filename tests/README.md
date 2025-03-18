# Testing Documentation

## Test Structure

### Unit Tests (`tests/unit/`)
- `test_transforms.py`: Tests individual transformation functions
- `test_config.py`: Tests configuration loading and validation

### Integration Tests (`tests/integration/`)
- `test_pipeline.py`: Tests complete pipeline flow

## Test Configuration
- Test configuration is stored in `tests/test_config.yml`
- Uses DuckDB for database operations
- Runs with local Spark instance

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/integration/test_pipeline.py

# Run with coverage report
pytest --cov=data_pipeline

# Run tests in parallel
pytest -n auto