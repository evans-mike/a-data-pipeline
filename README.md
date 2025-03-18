# A Data Pipeline
![Python](https://img.shields.io/badge/python-87.3%25-blue)
![Dockerfile](https://img.shields.io/badge/dockerfile-12.7%25-blue)

A data pipeline template for processing data using PySpark and Delta Lake, with local testing capabilities using DuckDB.

## Repository Information
- **Repository**: [evans-mike/a-data-pipeline](https://github.com/evans-mike/a-data-pipeline)
- **Last Updated**: 2025-03-18 20:43:27 UTC
- **Maintained by**: [@evans-mike](https://github.com/evans-mike)

## Table of Contents
1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Local Development](#local-development)
6. [Docker Setup](#docker-setup)
7. [Testing](#testing)
8. [Building and Deploying](#building-and-deploying)
9. [Configuration](#configuration)
10. [Contributing](#contributing)

## Overview
This project provides a template for building data pipelines that can:
- Run locally using Docker and DuckDB for testing
- Deploy to Databricks as a wheel package
- Use Delta Lake tables in production
- Implement both unit and integration tests
- Use dependency injection for database operations

## Prerequisites
- Python 3.9+
- Docker
- Databricks CLI (for deployment)
- Git

## Quick Start
```bash
# Clone the repository
git clone https://github.com/evans-mike/a-data-pipeline.git
cd a-data-pipeline

# Build Docker image
docker build -t pyspark-pipeline .

# Run tests
docker run --rm pyspark-pipeline pytest

# Build wheel package
python -m build
```

## Contributing

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

### Code Style
This project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

```bash
# Format code
black src/ tests/
isort src/ tests/
mypy src/
```

### Commit Messages
Please follow conventional commits format:
```
feat: add new transformation
fix: correct config loading
docs: update README
```

## License
[Add your chosen license]

## Acknowledgments
- PySpark Documentation
- Databricks Documentation
- Delta Lake Documentation

## Project Status
![Active Development](https://img.shields.io/badge/status-active-green)

Last updated: 2025-03-18 20:43:27 UTC by [@evans-mike](https://github.com/evans-mike)

### Working with Docker Containers

After building your image with `docker build -t pyspark-pipeline .`, you have several options for running containers:

1. **Run Interactive Development Session**
   ```bash
   # Start an interactive shell with current directory mounted
   docker run -it --rm \
     -v ${PWD}:/app \
     --name pyspark-dev \
     pyspark-pipeline /bin/bash
   ```
   - `-it`: Interactive terminal
   - `--rm`: Remove container when stopped
   - `-v ${PWD}:/app`: Mount current directory
   - `--name pyspark-dev`: Give container a recognizable name

2. **Run in Background Mode**
   ```bash
   # Start container in detached mode
   docker run -d \
     -v ${PWD}:/app \
     --name pyspark-service \
     pyspark-pipeline
   ```
   - `-d`: Run in detached (background) mode

3. **Run One-Off Commands**
   ```bash
   # Run tests
   docker run --rm pyspark-pipeline pytest

   # Run a specific Python script
   docker run --rm -v ${PWD}:/app pyspark-pipeline python src/your_package/pipeline/transforms.py
   ```

### Container Management Commands

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop a running container
docker stop pyspark-dev

# Start a stopped container
docker start pyspark-dev

# Attach to a running container
docker exec -it pyspark-dev /bin/bash

# View container logs
docker logs pyspark-dev

# Remove a container
docker rm pyspark-dev
```

### Development Workflow Example

1. **Start Development Container**
   ```bash
   docker run -it --rm \
     -v ${PWD}:/app \
     --name pyspark-dev \
     pyspark-pipeline /bin/bash
   ```

2. **Inside Container**
   - Run tests: `pytest`
   - Execute scripts: `python src/your_package/pipeline/transforms.py`
   - Install new packages: `pip install <package-name>`

3. **Code Changes**
   - Edit files on your local machine with your preferred editor
   - Changes are immediately reflected in the container
   - Run tests in container to verify changes

4. **Exit Container**
   - Type `exit` or press `Ctrl+D`
   - Container will automatically be removed (due to `--rm` flag)

### Platform-Specific Notes

**Windows:**
```bash
# Use this syntax for volume mounting
docker run -it --rm -v %cd%:/app pyspark-pipeline /bin/bash

# Or with PowerShell
docker run -it --rm -v ${PWD}:/app pyspark-pipeline /bin/bash
```

**Mac/Linux:**
```bash
docker run -it --rm -v $(pwd):/app pyspark-pipeline /bin/bash
```

### Common Issues and Solutions

1. **Volume Mount Issues**
   - Ensure you're in the project root directory
   - On Windows, check Docker Desktop file sharing settings
   - Use absolute paths if relative paths fail

2. **Permission Issues**
   ```bash
   # If you see permission errors, add your user to docker group (Linux)
   sudo usermod -aG docker $USER
   # Then log out and back in
   ```

3. **Container Won't Start**
   - Check if port is already in use
   - Ensure Docker Desktop is running
   - Check available system resources

## Building and Deploying the Wheel Package

### Local Build Process

1. **Install build tools**
   ```bash
   pip install build
   ```

2. **Build the wheel package**
   ```bash
   # From the project root directory
   python -m build

   # This will create two directories:
   # - dist/data_pipeline-0.1.0.tar.gz (source distribution)
   # - dist/data_pipeline-0.1.0-py3-none-any.whl (wheel distribution)
   ```

3. **Test the wheel locally**
   ```bash
   # Create a new virtual environment
   python -m venv test_env
   source test_env/bin/activate  # On Windows: test_env\Scripts\activate

   # Install the wheel
   pip install dist/data_pipeline-0.1.0-py3-none-any.whl
   ```

### Deploying to Databricks

1. **Upload wheel to Databricks**
   ```bash
   # Using Databricks CLI (ensure you're configured)
   databricks fs cp \
     dist/data_pipeline-0.1.0-py3-none-any.whl \
     dbfs:/FileStore/jars/data_pipeline-0.1.0-py3-none-any.whl
   ```

2. **Install on Databricks Cluster**
   - Go to your cluster configuration
   - Add the wheel to Libraries:
     ```
     dbfs:/FileStore/jars/data_pipeline-0.1.0-py3-none-any.whl
     ```
   - Restart the cluster

3. **Using in Databricks Notebook**
   ```python
   # Import and use the package
   from data_pipeline.pipeline import DataPipeline
   from data_pipeline.config import AppConfig

   # Initialize pipeline
   config = AppConfig.from_yaml("/dbfs/path/to/config.yml")
   pipeline = DataPipeline(config)

   # Run pipeline
   pipeline.run("source_table", "target_table")
   ```

### Version Management

Current build information:
- Build timestamp: 2025-03-18 20:35:08 UTC
- Built by: evans-mike
- Version: 0.1.0

### Build Dependencies

Make sure your `pyproject.toml` and `setup.py` are properly configured:

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

### Common Issues and Solutions

1. **Missing Dependencies**
   ```bash
   # Install all development dependencies
   pip install -e ".[dev]"
   ```

2. **Version Conflicts**
   - Check `pip freeze` output
   - Use `pip-compile` for deterministic builds
   ```bash
   pip install pip-tools
   pip-compile requirements.in
   ```

3. **Databricks Compatibility**
   - Ensure Python version matches cluster
   - Test with same Spark version as cluster
   - Verify all dependencies are available in Databricks

### Continuous Integration

Example GitHub Actions workflow for automated builds:

```yaml
name: Build and Test

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build
      - name: Build package
        run: python -m build
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/
```

### Local Development vs Deployment

1. **Local Testing**
   ```bash
   # Install in editable mode
   pip install -e ".[dev]"
   
   # Run tests
   pytest
   ```

2. **Production Deployment**
   ```bash
   # Build production wheel
   python -m build
   
   # Deploy to Databricks
   databricks fs cp [wheel-file] dbfs:/FileStore/jars/
   ```

### Version History

| Version | Date | Builder | Changes |
|---------|------|---------|---------|
| 0.1.0 | 2025-03-18 | evans-mike | Initial release |