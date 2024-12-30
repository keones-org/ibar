from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from .config import settings
from .models import CompletionRequest, CompletionResponse, ModelListResponse

app = FastAPI()

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

AVAILABLE_MODELS = [
    "deepseek-chat"
]

# Debug logging function
def log_request_details(model: str, headers: dict, payload: dict):
    print(f"\nMaking request to Deepseek API:")
    print(f"Model: {model}")
    print(f"API Key (first 8 chars): {headers['Authorization'][:14]}...")
    print(f"Payload: {payload}\n")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/api/models", response_model=ModelListResponse)
async def list_models():
    return {"models": AVAILABLE_MODELS}

@app.post("/api/completions", response_model=CompletionResponse)
async def create_completion(request: CompletionRequest):
    if request.model not in AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail="Invalid model selected")
    
    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare the context for FIM (Fill in Middle) if prefix/suffix are provided
    if request.prefix and request.suffix:
        prompt = f"{request.prefix}<fim_middle>{request.suffix}"
    else:
        prompt = request.prompt

    payload = {
        "model": request.model,
        "prompt": prompt,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens
    }

    # Mock response while waiting for API key
    if not settings.deepseek_api_key:
        # Simulate different responses based on the request
        if request.prefix and request.suffix:
            # FIM (Fill in Middle) mock response
            mock_text = "    return x + y  # Mock FIM completion"
        else:
            # Regular completion mock response
            mock_responses = {
                "Write a simple hello world in Python": 'print("Hello, World!")',
                "default": "# Mock response: This is a placeholder until we get the API key\ndef example():\n    pass"
            }
            mock_text = mock_responses.get(request.prompt, mock_responses["default"])
        
        return CompletionResponse(
            text=mock_text,
            model=request.model
        )
    
    # Real API call (when API key is available)
    async with httpx.AsyncClient() as client:
        try:
            # Prepare messages array with system and user messages
            messages = []
            
            # Add system message
            messages.append({
                "role": "system",
                "content": "You are a helpful assistant."
            })
            
            # Add user message
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Prepare API payload
            api_payload = {
                "model": request.model,
                "messages": messages,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens,
                "stream": False
            }

            print(f"Final payload: {api_payload}")
            
            response = await client.post(
                f"{settings.deepseek_api_base_url}/chat/completions",
                headers=headers,
                json=api_payload,
                timeout=30.0
            )
            response.raise_for_status()
            completion_data = response.json()
            
            # Extract the response text from chat completion
            response_text = completion_data["choices"][0]["message"]["content"]
            
            # For FIM responses, extract only the middle part if needed
            if request.prefix and request.suffix:
                # Try to extract the content between prefix and suffix
                try:
                    start = len(request.prefix)
                    end = response_text.index(request.suffix)
                    response_text = response_text[start:end].strip()
                except ValueError:
                    # If we can't find the suffix, return the whole response
                    pass
            
            return CompletionResponse(
                text=response_text,
                model=request.model
            )
        except httpx.HTTPError as e:
            # Log the error details for debugging
            error_msg = str(e)
            print(f"API Error: {error_msg}")
            
            if isinstance(e, httpx.HTTPStatusError):
                try:
                    error_detail = e.response.json() if e.response.headers.get("content-type") == "application/json" else {"error": {"message": error_msg}}
                except Exception:
                    error_detail = {"error": {"message": error_msg}}
                    
                    
                if e.response.status_code == 401:
                    error_detail = {"error": {"message": "Invalid API key or unauthorized access"}}
                elif e.response.status_code == 400 and "Model Not Exist" in error_msg:
                    error_detail = {"error": {"message": f"Invalid model: {request.model}. Please check available models using GET /api/models"}}
                    
                raise HTTPException(status_code=e.response.status_code, detail=error_detail)
            raise HTTPException(status_code=500, detail={"error": {"message": "Internal server error", "details": error_msg}})
