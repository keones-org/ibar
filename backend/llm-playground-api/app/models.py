from typing import List, Optional
from pydantic import BaseModel, field_validator, model_validator

class CompletionRequest(BaseModel):
    prompt: Optional[str] = None
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000
    prefix: Optional[str] = None
    suffix: Optional[str] = None

    @field_validator('model')
    @classmethod
    def validate_model(cls, v: str) -> str:
        if v != "deepseek-chat":
            raise ValueError('Invalid model: only "deepseek-chat" is supported')
        return v

    @model_validator(mode='after')
    def validate_completion_mode(self) -> 'CompletionRequest':
        has_prompt = self.prompt is not None
        has_prefix = self.prefix is not None
        has_suffix = self.suffix is not None
        has_fim = has_prefix and has_suffix

        if not has_prompt and not has_fim:
            raise ValueError('Either prompt or both prefix and suffix must be provided')
        
        if has_prompt and has_fim:
            raise ValueError('Cannot provide both prompt and prefix/suffix pair')
        
        return self

class CompletionResponse(BaseModel):
    text: str
    model: str

class ModelListResponse(BaseModel):
    models: List[str]
