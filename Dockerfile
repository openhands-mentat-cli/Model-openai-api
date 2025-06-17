# Root Dockerfile - Points to optimized railway-llm setup
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"
ENV FORCE_CMAKE=1

# Install system dependencies including ninja for llama-cpp-python compilation
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev \
    build-essential cmake pkg-config ninja-build \
    libopenblas-dev liblapack-dev \
    git wget curl gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the entire railway-llm setup
COPY railway-llm/ .

# Copy the frontend files
COPY frontend/ ./frontend/

# Upgrade pip and setuptools first
RUN pip3 install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Make scripts executable
RUN chmod +x *.sh

# Create model directory
RUN mkdir -p /app/models

# Download Phi-3-mini model (Q4_K_M quantization)
RUN python3 download_model.py

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the server with frontend
CMD ["./start_with_frontend.sh"]
