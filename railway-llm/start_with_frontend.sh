#!/bin/bash
set -e

echo "🚀 Starting Phi-3-mini 128k LLM Server with Frontend"
echo "===================================================="

# Configuration
export PORT=${PORT:-8000}
export HOST="0.0.0.0"
export MODEL_PATH="/app/models/phi-3-mini-128k-q4.gguf"

# CPU Optimization settings for Railway (8 vCPU)
export N_THREADS=8
export N_BATCH=512
export N_CTX=131072  # 128k context
export N_GPU_LAYERS=0  # CPU only

echo "🔧 Configuration:"
echo "   Port: $PORT"
echo "   Host: $HOST"
echo "   Model: $MODEL_PATH"
echo "   Threads: $N_THREADS"
echo "   Batch size: $N_BATCH"
echo "   Context length: $N_CTX tokens (128k)"
echo "   GPU layers: $N_GPU_LAYERS (CPU only)"
echo "   Frontend: Enabled at /frontend"

# Verify model exists
if [ ! -f "$MODEL_PATH" ]; then
    echo "❌ Model not found at $MODEL_PATH"
    echo "🔄 Attempting to download model..."
    python3 download_model.py
fi

# Check model size and available memory
if [ -f "$MODEL_PATH" ]; then
    MODEL_SIZE=$(du -h "$MODEL_PATH" | cut -f1)
    echo "📊 Model size: $MODEL_SIZE"
else
    echo "❌ Model still not found after download attempt"
    exit 1
fi

# Memory info (if available)
if command -v free >/dev/null 2>&1; then
    echo "💾 Available memory:"
    free -h
fi

echo "🚀 Starting integrated frontend server with llama-cpp-python backend..."

# Set API key for authentication
export API_KEY='Hello1'

echo "🔐 API Key authentication enabled"
echo "   API Key: Hello1"

# Start the integrated frontend server that manages llama-cpp-python internally
exec python3 frontend_server.py
