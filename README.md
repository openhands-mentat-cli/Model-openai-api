# Phi-3 Mini 128k on Railway

This repository contains everything needed to deploy Microsoft's Phi-3 Mini 128k model on Railway using Ollama with an OpenAI-compatible API.

## Features

- 🚀 One-click deployment to Railway
- 🔌 OpenAI-compatible API endpoints
- 💾 CPU-optimized performance
- 🔧 Automatic model downloading
- 📡 CORS enabled for web applications

## Model Specifications

- **Model**: Microsoft Phi-3 Mini 128k
- **Context Length**: 128,000 tokens
- **Parameters**: ~3.8B
- **Memory Usage**: ~2-4GB RAM
- **Deployment**: CPU-only optimized

## Railway Deployment

### Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

### Manual Deployment

1. Fork this repository
2. Connect your Railway account to GitHub
3. Create a new Railway project from this repository
4. Railway will automatically build and deploy using the Dockerfile
5. Wait for the model to download (first deployment takes ~10-15 minutes)

### Configuration

The deployment is configured through `railway.toml` with optimal settings for Railway's infrastructure:

- **Port**: 11434
- **Health Check**: `/api/tags`
- **Restart Policy**: On failure with 10 max retries
- **Build Timeout**: 300 seconds

## API Usage

Once deployed, your Railway app will provide an OpenAI-compatible API at:

```
https://your-app-name.railway.app/v1
```

### Chat Completions

```bash
curl -X POST "https://your-app-name.railway.app/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "phi3:mini-128k",
    "messages": [
      {
        "role": "user",
        "content": "Hello! Tell me about artificial intelligence."
      }
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

### Available Endpoints

- `GET /api/tags` - List available models
- `POST /v1/chat/completions` - Chat completions (OpenAI compatible)
- `POST /v1/completions` - Text completions (OpenAI compatible)
- `POST /api/generate` - Ollama native generate
- `POST /api/chat` - Ollama native chat

## Local Development

### Prerequisites

- Docker
- 8GB+ RAM recommended
- Internet connection for model download

### Run Locally

```bash
# Clone the repository
git clone <your-repo-url>
cd Model-openai-api

# Build the Docker image
docker build -t phi3-ollama .

# Run the container
docker run -p 11434:11434 phi3-ollama
```

The service will be available at `http://localhost:11434`

### Test the API

```bash
# Test the health endpoint
curl http://localhost:11434/api/tags

# Test chat completion
curl -X POST "http://localhost:11434/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "phi3:mini-128k",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Performance Optimization

The setup is optimized for Railway's CPU-only environment:

- Uses Ubuntu 22.04 base image for compatibility
- Ollama automatically handles model quantization
- CORS enabled for web application integration
- Health checks ensure reliable deployments

## Troubleshooting

### Common Issues

1. **Model Download Timeout**: First deployment may take 10-15 minutes for model download
2. **Memory Issues**: Phi-3 Mini requires ~2-4GB RAM, ensure sufficient resources
3. **Connection Issues**: Check that OLLAMA_ORIGINS is set to "*" for CORS

### Logs

Check Railway deployment logs for:
- Model download progress
- Server startup status
- API request logs

### Resource Monitoring

Monitor your Railway app's:
- Memory usage (should be ~2-4GB)
- CPU usage
- Network traffic

## Environment Variables

The following environment variables are configured:

- `OLLAMA_HOST`: Set to `0.0.0.0:11434`
- `OLLAMA_ORIGINS`: Set to `"*"` for CORS
- `PORT`: Set to `11434`

## Security Notes

- The API is configured to accept requests from any origin (`OLLAMA_ORIGINS="*"`)
- Consider implementing authentication for production use
- Monitor usage to prevent abuse

## License

This setup is provided as-is. Please check the licenses for:
- [Ollama](https://ollama.ai)
- [Microsoft Phi-3](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct)

## Support

For issues with:
- **Railway deployment**: Check Railway documentation
- **Ollama**: Check [Ollama GitHub](https://github.com/ollama/ollama)
- **Phi-3 model**: Check [Microsoft Phi-3 documentation](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct)
