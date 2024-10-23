from llms.LLM import LLM
from mistralai.client import MistralClient
from typing import List, Dict, Any, Optional
from utils.logger import Logger

class MistralApi(LLM):
    def __init__(self, api_key: str, model: str = "mistral-large-latest"):
        """
        Initialize the MistralApi with the given API key and model.

        Args:
            api_key (str): The API key for authentication with the Mistral API.
            model (str): The model to use for generating responses. Defaults to "mistral-large-latest".
        """
        self.client = MistralClient(api_key=api_key)
        self.model = model
        self.logger = Logger.get_logger(self)
        self.logger.debug('MistralApi initialized with model: %s', self.model)

    def chat(self, messages: List[Dict[str, Any]], options: Optional[Dict[str, Any]] = None) -> str:
        """
        Send a chat request to the Mistral API and return the response.

        Args:
            messages (List[Dict[str, Any]]): A list of message objects, where each message is a dictionary 
                                             with keys such as 'role' and 'content'.
            options (Optional[Dict[str, Any]]): Optional parameters for the chat request.

        Returns:
            str: The content of the response from the Mistral API.

        Raises:
            RuntimeError: If an error occurs while communicating with the Mistral API.
        """
        if options is None:
            options = {}
        
        self.logger.debug('Sending chat request to Mistral API with model: %s', self.model)
        self.logger.debug('Request messages: %s', messages)
        self.logger.debug('Request options: %s', options)
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=messages,
                **options
            )
            response_content = response.choices[0].message.content
            self.logger.debug('Received response from Mistral API: %s', response_content)
            return response_content
        except Exception as e:
            self.logger.error('Error occurred while communicating with the Mistral API: %s', e, exc_info=True)
            raise RuntimeError(f"An error occurred while communicating with the Mistral API: {e}")
