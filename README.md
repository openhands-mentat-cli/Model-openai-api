# Phi-3-mini 128k LLM Server

🤖 **High-Performance CPU-Optimized LLM Server with Web Interface**

This repository provides a production-ready Phi-3-mini 128k model server optimized for Railway deployment with an integrated web interface.

## ✨ Features

- 🧠 **Phi-3-mini 128k** - Microsoft's powerful small language model with 128k context length
- ⚡ **CPU Optimized** - llama.cpp with OpenBLAS optimizations for maximum performance
- 🔗 **OpenAI Compatible API** - Drop-in replacement for OpenAI API endpoints
- 🎯 **Q4_K_M Quantization** - Optimal balance of quality and memory usage
- 🌐 **Web Interface** - Built-in chat interface accessible at the root URL
- 🚀 **Railway Ready** - Configured for Railway's 8GB RAM / 8 vCPU environment

## 🚀 Quick Deploy to Railway

### One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/phi3-mini)

### Manual Deploy

1. **Fork this repository**
2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Railway will automatically detect the `railway.toml` configuration
3. **Deploy**: Railway will build and deploy automatically
4. **Wait**: Initial deployment takes 5-10 minutes (downloading ~2.4GB model)
5. **Access**: Open the provided Railway URL to access the web interface

## 🌐 Usage

### Web Interface
Once deployed, visit your Railway app URL to access the web interface with:
- **Chat Tab**: Interactive chat with the AI model
- **API Docs Tab**: Complete API documentation with examples
- **Status Tab**: System health and model information

### API Endpoints

**Base URL**: `https://your-railway-app.railway.app`

#### Chat Completions
```bash
curl -X POST "https://your-railway-app.railway.app/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $$Hello1$$" \
  -d '{
    "model": "phi-3-mini-128k",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

#### Health Check
```bash
curl https://your-railway-app.railway.app/health
```

#### List Models
```bash
curl https://your-railway-app.railway.app/v1/models
```

### Python Example
```python
import openai

client = openai.OpenAI(
    base_url="https://your-railway-app.railway.app/v1",
    api_key="$$Hello1$$"
)

response = client.chat.completions.create(
    model="phi-3-mini-128k",
    messages=[
        {"role": "user", "content": "Explain quantum computing"}
    ],
    max_tokens=1000
)

print(response.choices[0].message.content)
```

## 📊 System Requirements

**Railway Configuration:**
- **Memory**: 8GB (model uses ~4-5GB + overhead)
- **CPU**: 8 vCPU (fully utilized for inference)
- **Storage**: Model size ~2.4GB + dependencies
- **Build Time**: 5-10 minutes (includes model download)

## ⚙️ Configuration

The deployment is pre-configured with optimal settings:

- **Context Length**: 128k tokens
- **Quantization**: Q4_K_M
- **CPU Threads**: 8 (matches Railway vCPU count)
- **Batch Size**: 512 tokens
- **API Authentication**: Required (`$$Hello1$$`)

## 📈 Performance

**Expected Performance on Railway:**
- **Throughput**: ~10-20 tokens/second
- **Latency**: ~2-5 seconds for first token
- **Context**: Full 128k context supported
- **Concurrent Users**: 1-2 simultaneous (memory limited)

## 🔧 Customization

### Using Different Models
Edit `railway-llm/download_model.py` to use different GGUF models:

```python
model_info = {
    "repo_id": "microsoft/Phi-3-mini-128k-instruct-gguf",
    "filename": "Phi-3-mini-128k-instruct-q5.gguf",  # Higher quality
    "local_filename": "phi-3-mini-128k-q5.gguf"
}
```

### Performance Tuning
Edit `railway-llm/start_with_frontend.sh`:

```bash
export N_CTX=32768   # Smaller context for faster inference
export N_BATCH=1024  # Larger batch size for higher throughput
export N_THREADS=16  # Use hyperthreading if available
```

## 🚨 Troubleshooting

### Common Issues

**Build Fails**
- Check Railway logs for specific error messages
- Ensure repository structure is correct
- Verify `railway.toml` is in root directory

**Model Download Timeout**
- Railway build has 10-minute timeout
- Model download is ~2.4GB and usually completes in 2-3 minutes
- Check network connectivity in build logs

**Out of Memory**
- Reduce context length (`N_CTX`) in startup script
- Consider using smaller quantization (Q4_0 instead of Q4_K_M)
- Monitor Railway metrics for memory usage

**Slow Performance**
- Check CPU utilization in Railway metrics
- Ensure all 8 vCPUs are being utilized
- Consider reducing context length for faster inference

## 🔒 Security

- **API Key Authentication**: All API endpoints require authentication
- **Default API Key**: `$$Hello1$$` (change for production use)
- **HTTPS**: Railway provides automatic HTTPS termination
- **Container Isolation**: Model runs in isolated container environment

## 📚 Learn More

- [Phi-3 Model Documentation](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct)
- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Railway Documentation](https://docs.railway.app/)

---

**🚀 Ready to deploy your own Phi-3-mini 128k server with web interface on Railway!**
