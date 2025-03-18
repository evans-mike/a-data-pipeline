# Use Python 3.9 as base image (common version for compatibility)
FROM python:3.9-slim

# Install dependencies for adding new repository
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        ca-certificates \
        gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add Eclipse Temurin repository and install Java
RUN wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && \
    echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        temurin-11-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set Java home environment variable
ENV JAVA_HOME=/usr/lib/jvm/temurin-11-jre
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Verify Java installation and environment
RUN java -version && \
    echo "JAVA_HOME is set to: ${JAVA_HOME}"

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Command to run tests (can be overridden)
CMD ["pytest"]