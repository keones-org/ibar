# LLM Playground API

A FastAPI-based backend service that provides an API for interacting with the DeepSeek language models.

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Create a `.env` file with the following variables:
```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE_URL=https://api.deepseek.com
```

## API Endpoints

### Health Check
```
GET /healthz
```
Returns the health status of the API.

Response:
```json
{
  "status": "ok"
}
```

### List Available Models
```
GET /api/models
```
Returns a list of available DeepSeek models.

Response:
```json
{
  "models": ["deepseek-chat"]
}
```

### Create Completion
```
POST /api/completions
```
Generate completions using DeepSeek models.

Request Body:
```json
{
  "model": "string",         // Required: Model name (must be "deepseek-chat")
  "prompt": "string",        // Optional: Text prompt for completion
  "temperature": 0.7,        // Optional: Controls randomness (0.0 to 1.0)
  "max_tokens": 1000,        // Optional: Maximum tokens to generate
  "prefix": "string",        // Optional: Prefix for Fill-in-Middle (FIM)
  "suffix": "string"         // Optional: Suffix for Fill-in-Middle (FIM)
}
```

Note: Either `prompt` or both `prefix` and `suffix` must be provided, but not both.

Example Responses:

1. Regular Completion:
```json
{
  "text": "Here's a simple \"Hello, World!\" program in Python:\n\nprint(\"Hello, World!\")\n",
  "model": "deepseek-chat"
}
```

2. Fill-in-Middle (FIM) Completion:
```json
{
  "text": "def add(x, y):\n    return x + y\n",
  "model": "deepseek-chat"
}
```

Note: The actual response text may vary based on the model's output and temperature setting.

Error Responses:
- 422 Unprocessable Entity: Invalid model name or request validation error
  ```json
  {
    "detail": [
      {
        "type": "value_error",
        "loc": ["body", "model"],
        "msg": "Value error, Invalid model: only \"deepseek-chat\" is supported",
        "input": "invalid-model"
      }
    ]
  }
  ```
- 400 Bad Request: API-level errors
  ```json
  {
    "detail": {
      "error": {
        "message": "Error message from DeepSeek API",
        "type": "error_type",
        "code": "error_code"
      }
    }
  }
  ```
- 401 Unauthorized: Invalid API key
  ```json
  {
    "detail": {
      "error": {
        "message": "Invalid API key or unauthorized access"
      }
    }
  }
  ```
- 500 Internal Server Error: Unexpected server error
  ```json
  {
    "detail": {
      "error": {
        "message": "Internal server error",
        "details": "Error details"
      }
    }
  }
  ```

Note about FIM (Fill-in-Middle):
When using FIM functionality, the API will return a completion that includes the filled-in code between the prefix and suffix. The response might include additional explanatory text. To extract just the code, you may need to parse the response text.

## Development

Start the development server:
```bash
poetry run uvicorn app.main:app --reload
```

## Testing

Test the API endpoints:
```bash
# Health check
curl http://localhost:8000/healthz

# List models
curl http://localhost:8000/api/models

# Create completion
curl -X POST http://localhost:8000/api/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "prompt": "Hello!",
    "temperature": 0.7,
    "max_tokens": 100
  }'

# Test FIM (Fill-in-Middle)
curl -X POST http://localhost:8000/api/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "prefix": "def greet():",
    "suffix": "# End of function",
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## Error Handling

The API provides detailed error messages for common issues:

1. Invalid Model:
```json
{
  "detail": "Invalid model selected"
}
```

2. Missing Required Fields:
```json
{
  "detail": "Either prompt or both prefix and suffix must be provided"
}
```

3. API Errors:
```json
{
  "detail": {
    "error": {
      "message": "Error message from DeepSeek API",
      "type": "error_type",
      "code": "error_code"
    }
  }
}
```
