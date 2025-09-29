import google.generativeai as genai

genai.configure(api_key="AIzaSyBtcYwKghlA9nnvX7zsEyhS4Eki_1yc72s")

# List available models
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Model: {model.name}")