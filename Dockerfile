FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Create ollama user and directories
RUN useradd -m -s /bin/bash ollama
RUN mkdir -p /home/ollama/.ollama
RUN chown -R ollama:ollama /home/ollama/.ollama

# Set working directory
WORKDIR /app

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose the port
EXPOSE 11434

# Switch to ollama user
USER ollama

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_ORIGINS="*"

# Start the service
CMD ["/app/start.sh"]
