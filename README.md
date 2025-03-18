# PySpark Data Pipeline Project

This project template provides a structure for developing PySpark data pipelines that can be run both locally using Docker and deployed to Databricks as a wheel package.

## Project Structure

```
.
├── Dockerfile
├── README.md
├── requirements.txt
├── setup.py
├── src/
│   └── your_package/
│       ├── __init__.py
│       └── pipeline/
│           ├── __init__.py
│           └── transforms.py
└── tests/
    └── test_transforms.py
```

## Getting Started

### Prerequisites

- Docker Desktop ([Install Docker](https://docs.docker.com/get-docker/))
- Python 3.9+ (for local development outside Docker)
- Make (optional, but recommended for using Makefile commands)
- Git

### Local Development Setup

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. Build the Docker image (first time will take a few minutes):
   ```bash
   docker build -t pyspark-pipeline .
   ```

3. Verify the build was successful by running the tests:
   ```bash
   docker run pyspark-pipeline
   ```

4. Start an interactive development session:
   ```bash
   # On Windows:
   docker run -it --rm -v ${PWD}:/app pyspark-pipeline /bin/bash

   # On Mac/Linux:
   docker run -it --rm -v $(pwd):/app pyspark-pipeline /bin/bash
   ```

   The `-v` flag mounts your current directory into the container, allowing you to:
   - Edit files on your local machine
   - See changes immediately in the container
   - Persist changes even after the container stops

5. Inside the container, you can:
   - Run tests: `pytest`
   - Run individual Python files: `python src/your_package/pipeline/transforms.py`
   - Install additional packages: `pip install <package-name>`

### Development Workflow

1. Start the container (as shown in step 4 above)
2. Make changes to the code using your preferred editor on your local machine
3. Run tests in the container to verify changes
4. When done, exit the container with `exit` command
5. Container will automatically clean up, but your code changes are saved locally

### Rebuilding the Docker Image

You'll need to rebuild the Docker image if you:
- Modify the Dockerfile
- Update requirements.txt

To rebuild:
```bash
# Force a clean build (recommended when troubleshooting):
docker build --no-cache -t pyspark-pipeline .

# Normal rebuild:
docker build -t pyspark-pipeline .
```

### Common Docker Commands

```bash
# List running containers
docker ps

# Stop a running container
docker stop <container-id>

# Remove all stopped containers
docker container prune

# View Docker logs
docker logs <container-id>

# Remove an image (if you need to start fresh)
docker rmi pyspark-pipeline
```

### Troubleshooting Docker

1. If you see "permission denied" errors:
   - On Linux: prefix commands with `sudo`
   - On Windows: ensure Docker Desktop is running
   - Check file permissions in your project directory

2. If container fails to start:
   - Verify Docker Desktop is running
   - Try stopping and removing existing containers
   - Check available disk space

3. If volume mount isn't working:
   - Verify the path syntax for your OS
   - Ensure you're in the project root directory
   - On Windows, ensure file sharing is enabled in Docker Desktop

### Building the Wheel Package

To build the wheel package for Databricks deployment:

```bash
python -m build
```

The wheel file will be created in the `dist/` directory.

### Deploying to Databricks

1. Build your wheel package as described above
2. Upload the wheel file to Databricks
3. Install the package in your Databricks cluster using `%pip install /dbfs/path/to/your-package.whl`

## Development Guidelines

### Code Structure

- Place your main pipeline code in `src/your_package/pipeline/`
- Write tests in the `tests/` directory
- Use `black` for code formatting and `isort` for import sorting

### Testing

Run tests locally using:

```bash
docker run pyspark-pipeline pytest
```

### Best Practices

1. Always write tests for new functionality
2. Keep transforms modular and composable
3. Use type hints in Python code
4. Document your functions and classes
5. Update requirements.txt when adding new dependencies

## Creating a New Pipeline

1. Create a new module in `src/your_package/pipeline/`
2. Write your transformation logic
3. Add corresponding tests
4. Build and test locally using Docker
5. When ready, build the wheel package and deploy to Databricks

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests and ensure they pass
4. Submit a pull request

## License

