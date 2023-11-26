from typing import List, Dict
from datetime import datetime

class Result:
    def __init__(self, status_code:int, message:str = '', data:List[Dict]=None):
        """
        Constructor for Result
        :param status_code: The HTTP status code from the response.
        :param message: The message from the JSON Response.
        :param data: The response deserialized to python object.
        """
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []

class GenerateCompletion:
    def __init__(self, model: str = '', created_at: datetime = datetime.now(), response: str = '', context: List[int] = [], done: bool = False, total_duration: int = 0, load_duration: int = 0, sample_count: int = 0, sample_duration: int = 0, prompt_eval_count: int = 0, prompt_eval_duration: int = 0, eval_count: int = 0, eval_duration: int = 0, **kwargs) -> None:
        self.model = model
        self.created_at = created_at
        self.response = response
        self.context = context
        self.done = done
        self.total_duration = total_duration
        self.load_duration = load_duration
        self.sample_count = sample_count
        self.sample_duration = sample_duration
        self.prompt_eval_count = prompt_eval_count
        self.prompt_eval_duration = prompt_eval_duration
        self.eval_count = eval_count
        self.eval_duration = eval_duration
        self.__dict__.update(kwargs)