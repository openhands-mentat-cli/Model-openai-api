# Phi-3-mini 128k LLM Server - Railway Deployment

🤖 **High-Performance CPU-Optimized LLM Server with OpenAI-Compatible API**

This deployment provides a production-ready Phi-3-mini 128k model server optimized for Railway's CPU-only environment.

## ✨ Features

- 🧠 **Phi-3-mini 128k** - Microsoft's powerful small language model with 128k context
- ⚡ **CPU Optimized** - llama.cpp with OpenBLAS optimizations for maximum performance
- 🔗 **OpenAI Compatible** - Drop-in replacement for OpenAI API endpoints
- 🎯 **Q4_K_M Quantization** - Optimal balance of quality and memory usage
- 🚀 **Railway Ready** - Configured for Railway's 8GB RAM / 8 vCPU environment

## 🚀 Quick Deploy to Railway

### Option 1: One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

### Option 2: Manual Deploy

1. **Fork this repository**
2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Select the `railway-llm` folder
3. **Deploy**: Railway will build and deploy automatically
4. **Wait**: Initial deployment takes 5-10 minutes (downloading model)

## 📋 System Requirements

**Railway Configuration:**
- **Memory**: 8GB (model uses ~4-5GB + overhead)
- **CPU**: 8 vCPU (fully utilized for inference)
- **Storage**: 100GB (model is ~2.4GB + dependencies)
- **Network**: HTTP/HTTPS on Railway-assigned port

## 🔌 API Usage

Once deployed, you can use the OpenAI-compatible API:

### Base URL
```
https://your-railway-app.railway.app
```

### Chat Completions
```bash
curl -X POST "https://your-railway-app.railway.app/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $$Hello1$$" \
  -d '{
    "model": "phi-3-mini-128k",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

### Python Example
```python
import openai

# Configure client to use your Railway deployment
client = openai.OpenAI(
    base_url="https://your-railway-app.railway.app/v1",
    api_key="$$Hello1$$"  # API key required
)

response = client.chat.completions.create(
    model="phi-3-mini-128k",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."}
    ],
    max_tokens=1000,
    temperature=0.7
)

print(response.choices[0].message.content)
```

### JavaScript/Node.js Example
```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: 'https://your-railway-app.railway.app/v1',
  apiKey: '$$Hello1$$', // API key required
});

async function chat() {
  const completion = await openai.chat.completions.create({
    model: 'phi-3-mini-128k',
    messages: [
      { role: 'system', content: 'You are a helpful assistant.' },
      { role: 'user', content: 'Explain machine learning basics.' }
    ],
    max_tokens: 800,
    temperature: 0.7,
  });

  console.log(completion.choices[0].message.content);
}

chat();
```

## 🔧 Available Endpoints

- `GET /health` - Health check endpoint
- `GET /v1/models` - List available models
- `POST /v1/chat/completions` - Chat completions (main endpoint)
- `POST /v1/completions` - Text completions
- `GET /docs` - API documentation (Swagger UI)

## ⚙️ Configuration

### Model Settings
- **Model**: Phi-3-mini 128k Instruct (Q4_K_M quantized)
- **Context Length**: 131,072 tokens (128k)
- **Quantization**: Q4_K_M (4-bit with K-means optimization)
- **Memory Usage**: ~4-5GB RAM
- **Chat Format**: ChatML

### Performance Optimizations
- **CPU Threads**: 8 (matches Railway vCPUs)
- **Batch Size**: 512 tokens
- **OpenBLAS**: Enabled for fast matrix operations
- **Interrupt Requests**: Enabled for responsive API

## 📊 Performance Expectations

**Railway 8 vCPU / 8GB RAM:**
- **Throughput**: ~10-20 tokens/second
- **Latency**: ~2-5 seconds for first token
- **Context**: Full 128k context supported
- **Concurrent Requests**: 1-2 simultaneous (memory limited)

## 🔍 Monitoring & Debugging

### Health Check
```bash
curl https://your-railway-app.railway.app/health
```

### View Available Models
```bash
curl https://your-railway-app.railway.app/v1/models
```

### Railway Logs
- Check Railway dashboard for deployment and runtime logs
- Model download progress is logged during initial deployment
- API request logs are available in real-time

## 🛠️ Customization

### Using Different Models

Edit `download_model.py` to use different models:

```python
# For Q5_K_M (higher quality, more RAM)
model_info = {
    "repo_id": "microsoft/Phi-3-mini-128k-instruct-gguf",
    "filename": "Phi-3-mini-128k-instruct-q5.gguf",
    "local_filename": "phi-3-mini-128k-q5.gguf"
}

# For other models (e.g., Llama, Mistral)
model_info = {
    "repo_id": "some-org/some-model-gguf",
    "filename": "model-q4_k_m.gguf",
    "local_filename": "custom-model.gguf"
}
```

### Performance Tuning

Edit `start.sh` for different configurations:

```bash
# For more aggressive CPU usage
export N_THREADS=16  # Use hyperthreading

# For lower memory usage
export N_CTX=32768   # 32k context instead of 128k

# For higher throughput
export N_BATCH=1024  # Larger batch size
```

## 🚨 Troubleshooting

### Common Issues

**Model Download Fails**
- Check Railway logs for network issues
- Verify Hugging Face Hub access
- Model download may take 5-10 minutes

**Out of Memory Errors**
- Reduce `N_CTX` (context length)
- Use Q4_0 quantization instead of Q4_K_M
- Reduce `N_BATCH` size

**Slow Response Times**
- Check CPU utilization in Railway metrics
- Reduce context length for faster inference
- Consider using smaller batch sizes

**API Not Responding**
- Verify health check endpoint works
- Check if model loaded successfully in logs
- Ensure Railway assigned port is correct

### Performance Tips

1. **Context Length**: Use only what you need - smaller context = faster inference
2. **Batch Size**: Tune based on your use case (512-1024 optimal)
3. **Quantization**: Q4_K_M is best balance; Q5_K_M for quality; Q4_0 for speed
4. **Concurrent Requests**: Limit to 1-2 to avoid memory issues

## 📚 Additional Resources

- [llama.cpp Documentation](https://github.com/ggerganov/llama.cpp)
- [Phi-3 Model Documentation](https://huggingface.co/microsoft/Phi-3-mini-128k-instruct)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Railway Documentation](https://docs.railway.app/)

## 🔒 Security Notes

- **API Key Authentication**: Required for all API requests
- **API Key**: `$$Hello1$$` (configured for easy access)
- **HTTPS**: Railway provides HTTPS termination automatically
- **Isolation**: Model runs in isolated container environment
- **Production**: Consider using environment-specific API keys for production

---

**🚀 Ready to run Phi-3-mini 128k with optimal CPU performance on Railway!**
