from pydantic import BaseModel

class PromptMessage(BaseModel):
  prompt: str
  kcal: str

class Message(BaseModel):
  text: str