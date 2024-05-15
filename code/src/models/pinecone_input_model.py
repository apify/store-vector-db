# generated by datamodel-codegen:
#   filename:  input_schema.json
#   timestamp: 2024-05-14T14:14:09+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Embeddings(Enum):
    OpenAIEmbeddings = 'OpenAIEmbeddings'
    HuggingFaceEmbeddings__CohereEmbeddings = 'HuggingFaceEmbeddings, CohereEmbeddings'


class PineconeIntegration(BaseModel):
    pinecone_index_name: str = Field(
        ..., description='Pinecone index name.', title='Pinecone index name'
    )
    pinecone_api_key: str = Field(
        ..., description='Pinecone API KEY', title='Pinecone API KEY'
    )
    embeddings: Embeddings = Field(
        ...,
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
        description='A list of fields which should be selected from the items, only these fields will remain in the resulting record objects.\n\n For example, when using the website content crawler, you might select fields such as `text` and `url`, and `metadata.title` among others, to be included in the vector store file.',
        title='A list of fields which should be selected from the items',
    )
    metadata_fields: Optional[Dict[str, Any]] = Field(
        None,
        description='A list of fields which should be selected from the items and stored as metadata. \n\n For example, when using the website content crawler, you might want to store `url` in metadata. In this case, use `metadata_fields parameter as follows {"page_url": "url"}`',
        title='Metadata fields',
    )
    metadata_values: Optional[Dict[str, Any]] = Field(
        None,
        description='Custom values to be stored for every Dataset item as metadata.\n\n For example, you might want to store `domain` in metadata, hence use `metadata_values as {"domain": "apify.com"}`',
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
