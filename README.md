# PySpark Data Pipeline Project

[previous sections remain the same...]

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

[rest of README remains the same...]