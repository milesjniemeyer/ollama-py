import requests
from urllib.parse import urljoin

class OllamaAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    # Helper function that uses requests to make the API calls
    def _make_request(self, method, endpoint, data=None):
        headers = { "Content-Type": "application/json" }
        url = urljoin(self.base_url, endpoint)

        try:
            response = requests.request(method, url, json=data, headers=headers)
            response.raise_for_status()

            if response.content:
                return response.json()
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f'Error making API request: {e}')
            if 'response' in locals() and hasattr(response, 'status_code'):
                print(f'HTTP Status Code: {response.status_code}')
                print(f'Response content: {response.content}')
            return None

    # Generates a completion by taking in a model and prompt
    def generate_completion(self, model:str, prompt:str, format:str=None, options:str=None, system:str=None, template:str=None, context:str=None, stream:bool=False, raw:str=False):
        endpoint = 'api/generate'
        payload = {
            "model": model,
            "prompt": prompt,
            "format": format,
            "options": options,
            "system": system,
            "template": template,
            "context": context,
            "stream": stream,
            "raw": raw
        }

        return self._make_request('POST', endpoint, data=payload)
    
    def create_model(self, name:str, path:str, stream:bool=False):
        endpoint = 'api/create'
        payload = {
            "name": name,
            "path": path,
            "stream": stream
        }

        return self._make_request('POST', endpoint, data=payload)
    
    def list_models(self):
        endpoint = 'api/tags'

        return self._make_request('GET', endpoint)
    
    def model_info(self, name:str):
        endpoint = 'api/show'
        payload = {
            "name": name
        }

        return self._make_request('POST', endpoint, data=payload)
    
    def copy_model(self, source:str, destination:str):
        endpoint = 'api/copy'
        payload = {
            "source": source,
            "destination": destination
        }

        return self._make_request('POST', endpoint, data=payload)
    
    # Response
    def delete_model(self, name:str):
        endpoint = 'api/delete'
        payload = {
            "name": name
        }

        return self._make_request('DELETE', endpoint, data=payload)

    # Work in progress
    def pull_model(self, name:str, insecure:bool=False, stream:bool=False):
        endpoint = 'api/pull'
        payload = {
            "name": name
            #"insecure": insecure,
            #"stream": stream
        }

        return self._make_request('POST', endpoint, data=payload)