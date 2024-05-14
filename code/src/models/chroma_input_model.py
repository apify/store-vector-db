# generated by datamodel-codegen:
#   filename:  input_schema.json
#   timestamp: 2024-05-14T13:42:45+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Embeddings(Enum):
    OpenAIEmbeddings = 'OpenAIEmbeddings'
    HuggingFaceEmbeddings__CohereEmbeddings = 'HuggingFaceEmbeddings, CohereEmbeddings'


class ChromaIntegration(BaseModel):
    chroma_collection_name: Optional[str] = Field(
        'chroma',
        description='Chroma DB collection name',
        title='Chroma DB collection name',
    )
    chroma_client_host: str = Field(
        ..., description='Host argument for ChromaDB HTTP Client', title='ChromaDB host'
    )
    chroma_client_port: Optional[int] = Field(
        8080,
        description='Port argument for ChromaDB HTTP Client',
        title='ChromaDB port',
    )
    chroma_client_ssl: Optional[bool] = Field(
        False, description='Enable/Disable SSL', title='ChromDB SSL'
    )
    chroma_server_auth_credentials: Optional[str] = Field(
        None,
        description='ChromaDB server Auth Static API token.',
        title='ChromaDB server auth Static API token credentials',
    )
    embeddings: Optional[Embeddings] = Field(
        None,
        description='Choose the embeddings provider to use for generating embeddings',
        title='Embeddings provider (as defined in the langchain API)',
    )
    embeddings_config: Optional[Dict[str, Any]] = Field(
        None,
        description='Specific configuration for the embeddings. For example, for OpenAI, you can the model name as ({"model": "text-embedding-ada-002"}), for HuggingFace ({"model_name": "sentence-transformers/paraphrase-MiniLM-L6-v2"})',
        title='Embeddings provider configuration',
    )
    embeddings_api_key: Optional[str] = Field(
        None,
        description='Value of the API KEY for the embeddings provider (if required).\n\n For example for OpenAI it is OPENAI_API_KEY, for Cohere it is COHERE_API_KEY)',
        title='Embeddings API KEY (whenever applicable, depends on provider)',
    )
    fields: List = Field(
        ...,
        description="Specify Dataset fields for text extraction in this array, using dot notation. \n\nE.g., for a crawler's 'text' output field, simply add 'text' to the array.",
        title='Fields',
    )
    metadata_fields: Optional[Dict[str, Any]] = Field(
        None,
        description='Select metadata fields (supports dot notation)',
        title='Metadata fields',
    )
    metadata_values: Optional[Dict[str, Any]] = Field(
        None,
        description='Custom values saved to db for every Dataset item as metadata',
        title='Metadata values',
    )
    perform_chunking: Optional[bool] = Field(
        False,
        description='If set to true, the resulting text will be chunked according to the settings below',
        title='Perform chunking',
    )
    chunk_size: Optional[int] = Field(
        1000,
        description='The maximum character length of each text chunk',
        ge=1,
        title='Chunk size',
    )
    chunk_overlap: Optional[int] = Field(
        0,
        description='The character overlap between text chunks that are next to each other',
        ge=0,
        title='Chunk overlap',
    )
    dataset_id: Optional[str] = Field(
        None,
        description='Dataset ID (when running standalone without integration)',
        title='Dataset ID',
    )
