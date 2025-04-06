import google.generativeai as genai

genai.configure(api_key="AIzaSyCdZELApwIv8f7ZmMtJhnr248fvhNs45g0")

# Convert generator to a list and print the model names
models = list(genai.list_models())
for model in models:
    print(model.name)
