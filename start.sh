#!/bin/bash
set -e

echo "Starting Ollama server..."

# Start Ollama in the background
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to be ready..."
# Wait for Ollama to be ready
until curl -f http://localhost:11434/api/tags >/dev/null 2>&1; do
    echo "Waiting for Ollama server to start..."
    sleep 2
done

echo "Ollama server is ready!"

# Pull the Phi-3 Mini 128k model
echo "Pulling Phi-3 Mini 128k model..."
ollama pull phi3:mini-128k

echo "Model pulled successfully!"
echo "Ollama server is running on http://0.0.0.0:11434"
echo "OpenAI-compatible API available at http://0.0.0.0:11434/v1"

# Keep the script running
wait $OLLAMA_PID
