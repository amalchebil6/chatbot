import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI configuration

PINECONE_API_KEY=os.getenv('PINECONE_API_KEY')

# Directory for legal documents
MISTRAL_KEY = os.getenv('MISTRAL_KEY')
COHERE_RERANKER_KEY = os.getenv('COHERE_RERANKER_KEY')
COHERE_RERANKER_COMPLETITIONS_ENDPOINT = os.getenv('COHERE_RERANKER_COMPLETITIONS_ENDPOINT')

MONGO_URI = os.getenv('MONGO_URI')

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'