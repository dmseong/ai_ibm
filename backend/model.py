from pydantic import BaseModel

class PromptMessage(BaseModel):
  prompt: str
  kcal: int

class Message(BaseModel):
  text: str