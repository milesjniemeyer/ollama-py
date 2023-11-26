import requests
import requests.packages
import logging
from typing import List, Dict
from json import JSONDecodeError
from .exceptions import OllamaAPIException
from .models import Result

class RestAdapter:
    def __init__(self, hostname:str='http://localhost:11434', logger:logging.Logger = None):
        """
        Constructor for RestAdapter
        :param hostname: (optional) The URL where your Ollama API instance is located. Defaults to http://localhost:11434.
        :param logger: (optional) If your app has a logger, pass it here.
        """
        self.hostname = hostname
        self._logger = logger or logging.getLogger(__name__)

    def _do(self, method:str, endpoint:str, data:Dict=None) -> Result:
        """
        Requests helper method
        :param method: The HTTP method being used.
        :param endpoint: The endpoint being accessed on the Ollama API (e.g. /api/tags).
        :param data: (optional) The body payload being passed to the Ollama API for certain endpoints.
        """
        full_url = self.hostname + endpoint
        headers = {'Content-Type': 'application/json'}

        log_line_pre = f'method={method}, url={full_url}'
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=method, url=full_url, headers=headers, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise OllamaAPIException('Request failed') from e
        
        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            json_response = response.json()
        except (ValueError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, None, e))
            raise OllamaAPIException('Bad JSON in response') from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200 
        log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=json_response)
        
        self._logger.error(msg=log_line)
        raise OllamaAPIException(f"{response.status_code}: {response.reason}")

    def get(self, endpoint:str) -> Result:
        """
        Requests GET method
        :param endpoint: The endpoint being accessed on the Ollama API (e.g. /api/tags).
        """
        return self._do(method='GET', endpoint=endpoint)
    
    def post(self, endpoint:str, data:Dict=None) -> Result:
        """
        Requests POST method
        :param endpoint: The endpoint being accessed on the Ollama API (e.g. /api/tags).
        :param data: (optional) The body payload being passed to the Ollama API for certain endpoints.
        """
        return self._do(method='POST', endpoint=endpoint, data=data)
    
    def delete(self, endpoint:str, data:Dict=None) -> Result:
        """
        Requests DELETE method
        :param endpoint: The endpoint being accessed on the Ollama API (e.g. /api/tags).
        :param data: (optional) The body payload being passed to the Ollama API for certain endpoints.
        """
        return self._do(method='DELETE', endpoint=endpoint, data=data)