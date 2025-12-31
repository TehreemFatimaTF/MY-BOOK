import google.generativeai as genai
import os
import sys

sys.path.append(os.getcwd())
from src.config.settings import settings

genai.configure(api_key=settings.gemini_api_key)

print("Listing models:")
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
