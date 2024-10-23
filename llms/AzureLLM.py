from typing import List, Dict, Any
from openai import AzureOpenAI
from llms.LLM import LLM
from utils.logger import Logger
import time

class AzureLLM(LLM):
    def __init__(self, api_key: str, model: str, azure_endpoint: str, api_version: str = "2024-02-01", options: Dict[str, Any] = None):
        """
        Initialize the Azure LLM with the OpenAI client.

        Args:
            api_key (str): The API key for authentication.
            model (str): The model name to use for completion.
            azure_endpoint (str): The Azure endpoint for the OpenAI service.
            api_version (str): The API version to use. Default is "2024-02-01".
            options (Dict[str, Any]): Optional parameters for the API request.
        """
        super().__init__(model)
        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=api_version
        )
        self.options = options if options is not None else {}
        self.logger = Logger.get_logger(self)

    def chat(self, messages: List[Dict[str, Any]], max_retries: int = 3, initial_delay: float = 30.0, backoff_factor: float = 2.0) -> str:
        """
        Get a chat completion from the Azure OpenAI service with a retry mechanism.

        Args:
            messages (List[Dict[str, Any]]): The messages to send to the model.
            max_retries (int): The maximum number of retries. Default is 5.
            initial_delay (float): The initial delay between retries in seconds. Default is 1.0.
            backoff_factor (float): The factor by which the delay increases after each retry. Default is 2.0.

        Returns:
            str: The model's response message.
        """
        self.logger.debug('Sending chat request with messages: %s', messages)
        attempt = 0
        delay = initial_delay

        while attempt < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    **self.options
                )
                self.logger.debug('Received response: %s', response)
                return response.choices[0].message
            except Exception as e:
                attempt += 1
                self.logger.error('Error during chat completion: %s', e, exc_info=True)
                if attempt >= max_retries:
                    raise
                else:
                    self.logger.info('Retrying chat completion in %s seconds...', delay)
                    time.sleep(delay)
                    delay *= backoff_factor
