#!/usr/bin/env python3
"""
Frontend server that serves static files and proxies API requests to llama-cpp-python server.
This allows serving the web interface alongside the LLM API.
"""

import os
import asyncio
import subprocess
import time
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
import httpx
import uvicorn
from contextlib import asynccontextmanager

# Configuration
API_PORT = 8001  # Port for llama-cpp-python server
FRONTEND_PORT = int(os.getenv('PORT', 8000))  # Port for this frontend server
HOST = "0.0.0.0"
MODEL_PATH = "/app/models/phi-3-mini-128k-q4.gguf"
API_KEY = "Hello1"

# CPU Optimization settings
N_THREADS = 8
N_BATCH = 512
N_CTX = 131072  # 128k context
N_GPU_LAYERS = 0  # CPU only

llama_process = None

async def start_llama_server():
    """Start the llama-cpp-python server in the background."""
    global llama_process
    
    print("🚀 Starting llama-cpp-python server...")
    
    # Build the command
    cmd = [
        "python3", "-m", "llama_cpp.server",
        "--model", MODEL_PATH,
        "--host", "127.0.0.1",  # Only bind to localhost for internal use
        "--port", str(API_PORT),
        "--n_threads", str(N_THREADS),
        "--n_batch", str(N_BATCH),
        "--n_ctx", str(N_CTX),
        "--n_gpu_layers", str(N_GPU_LAYERS),
        "--chat_format", "chatml",
        "--api_key", API_KEY
    ]
    
    print(f"📝 Command: {' '.join(cmd)}")
    
    # Start the process with real-time output
    llama_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    # Wait for the server to start with better error handling
    print("⏳ Waiting for llama-cpp-python server to start...")
    
    # Start a task to read and print output
    async def read_output():
        while llama_process.poll() is None:
            try:
                line = llama_process.stdout.readline()
                if line:
                    print(f"[llama-cpp] {line.strip()}")
            except:
                break
            await asyncio.sleep(0.1)
    
    output_task = asyncio.create_task(read_output())
    
    # Wait up to 180 seconds (3 minutes) for large models
    for i in range(180):
        # Check if process died
        if llama_process.poll() is not None:
            output_task.cancel()
            returncode = llama_process.returncode
            print(f"❌ llama-cpp-python process exited with code {returncode}")
            
            # Try to get any remaining output
            try:
                remaining_output = llama_process.stdout.read()
                if remaining_output:
                    print(f"[llama-cpp] {remaining_output}")
            except:
                pass
            
            raise Exception(f"llama-cpp-python server process exited with code {returncode}")
        
        # Try health check first, then fallback to models endpoint
        try:
            async with httpx.AsyncClient() as client:
                # Try health endpoint first
                try:
                    response = await client.get(f"http://127.0.0.1:{API_PORT}/health", timeout=5.0)
                    if response.status_code == 200:
                        print("✅ llama-cpp-python server is ready! (health check)")
                        output_task.cancel()
                        return
                except:
                    # Health endpoint might not exist, try models endpoint
                    response = await client.get(
                        f"http://127.0.0.1:{API_PORT}/v1/models", 
                        headers={"Authorization": f"Bearer {API_KEY}"},
                        timeout=5.0
                    )
                    if response.status_code == 200:
                        print("✅ llama-cpp-python server is ready! (models endpoint)")
                        output_task.cancel()
                        return
        except Exception as e:
            # Only print connection errors every 30 seconds to avoid spam
            if i % 30 == 0 and i > 0:
                print(f"⏳ Still waiting... (attempt {i}/180) - {str(e)}")
        
        await asyncio.sleep(1)
    
    output_task.cancel()
    
    # If we get here, the server didn't start in time
    if llama_process.poll() is None:
        print("❌ Timeout waiting for llama-cpp-python server to start")
        llama_process.terminate()
        try:
            llama_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            llama_process.kill()
    
    raise Exception("Failed to start llama-cpp-python server within timeout")

async def stop_llama_server():
    """Stop the llama-cpp-python server."""
    global llama_process
    if llama_process:
        print("🛑 Stopping llama-cpp-python server...")
        llama_process.terminate()
        try:
            llama_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            llama_process.kill()
        llama_process = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifecycle of the llama-cpp-python server."""
    await start_llama_server()
    yield
    await stop_llama_server()

# Create FastAPI app
app = FastAPI(
    title="Phi-3-mini 128k LLM Server with Frontend",
    description="OpenAI-compatible API with web interface",
    lifespan=lifespan
)

# Mount static files
frontend_path = Path(__file__).parent.parent / "frontend"  # Go up one level to /app/frontend
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the main frontend page."""
    frontend_file = Path(__file__).parent.parent / "frontend" / "index.html"  # Go up one level to /app/frontend
    if frontend_file.exists():
        return FileResponse(str(frontend_file))
    else:
        raise HTTPException(status_code=404, detail="Frontend not found")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        async with httpx.AsyncClient() as client:
            # Try health endpoint first
            try:
                response = await client.get(f"http://127.0.0.1:{API_PORT}/health", timeout=5.0)
                if response.status_code == 200:
                    return {"status": "healthy", "llama_server": True, "method": "health"}
            except:
                pass
            
            # Fallback to models endpoint
            response = await client.get(
                f"http://127.0.0.1:{API_PORT}/v1/models",
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=5.0
            )
            if response.status_code == 200:
                return {"status": "healthy", "llama_server": True, "method": "models"}
            else:
                return {"status": "unhealthy", "llama_server": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "unhealthy", "llama_server": False, "error": str(e)}

@app.api_route("/v1/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_to_llama(request: Request, path: str):
    """Proxy all /v1/* requests to the llama-cpp-python server."""
    url = f"http://127.0.0.1:{API_PORT}/v1/{path}"
    
    # Get request body
    body = await request.body()
    
    # Forward the request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers=dict(request.headers),
                content=body,
                timeout=300.0  # 5 minute timeout for long generations
            )
            
            # Return the response
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Phi-3-mini 128k LLM Server with Frontend")
    print("====================================================")
    print(f"🔧 Configuration:")
    print(f"   Frontend Port: {FRONTEND_PORT}")
    print(f"   API Port: {API_PORT} (internal)")
    print(f"   Host: {HOST}")
    print(f"   Model: {MODEL_PATH}")
    print(f"   Threads: {N_THREADS}")
    print(f"   Batch size: {N_BATCH}")
    print(f"   Context length: {N_CTX} tokens (128k)")
    print(f"   GPU layers: {N_GPU_LAYERS} (CPU only)")
    print(f"   Frontend: Enabled at /")
    print(f"🔐 API Key: {API_KEY}")
    
    # Verify model exists
    if not os.path.exists(MODEL_PATH):
        print("❌ Model not found, downloading...")
        subprocess.run(["python3", "download_model.py"], check=True)
    
    # Start the server
    uvicorn.run(
        app,
        host=HOST,
        port=FRONTEND_PORT,
        log_level="info"
    )