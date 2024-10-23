import anthropic
from llms.LLM import LLM
from utils.logger import Logger
from typing import List, Dict, Any, Optional

class ClaudeLLM(LLM):
    def __init__(self, api_key: str, options: Optional[Dict[str, Any]] = None, model: str = "claude-3-5-sonnet-20240620"):
        """
        Initialize the Claude LLM with the Anthropic client.

        Args:
            api_key (str): The API key for authentication.
            options (Optional[Dict[str, Any]]): Optional parameters for the API request.
            model (str): The model name to use for completion. Default is "claude-3-5-sonnet-20240620".
        """
        self.options = options if options is not None else {}
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.logger = Logger.get_logger(self)

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        """
        Get a chat completion from the Anthropic Claude service.

        Args:
            messages (List[Dict[str, Any]]): The messages to send to the model.

        Returns:
            str: The model's response message.
        """
        self.logger.debug('Sending chat request with messages: %s', messages)
        
        # Handling the message structure
        system_message = messages[0]["content"] if messages[0]["role"] == "system" else None
        user_messages = messages[1:] if messages[0]["role"] == "system" else messages
        
        try:
            response = self.client.messages.create(
                model=self.model,
                system=system_message,
                messages=user_messages,
                **self.options
            )
            self.logger.debug('Received response: %s', response)
            return response.content[0].text
        except Exception as e:
            self.logger.error('Error during chat completion: %s', e, exc_info=True)
            raise
