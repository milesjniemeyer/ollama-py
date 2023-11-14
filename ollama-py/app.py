from ollamaapi import OllamaAPI

url = 'http://localhost:11434'

ollama_api = OllamaAPI(url)

prompt = "What was perestroika?"
get_response = ollama_api.generate_completion('orca-mini:3b', prompt)
print(get_response['response'])