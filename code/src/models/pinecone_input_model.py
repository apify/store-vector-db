# generated by datamodel-codegen:
#   filename:  input_schema.json
#   timestamp: 2024-06-05T12:08:31+00:00

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EmbeddingsProvider(Enum):
    OpenAIEmbeddings = 'OpenAIEmbeddings'
    CohereEmbeddings = 'CohereEmbeddings'


class PineconeIntegration(BaseModel):
    pineconeIndexName: str = Field(
        ...,
        description='Name of the Pinecone index where the data will be stored',
        title='Pinecone index name',
    )
    pineconeApiKey: str = Field(
        ..., description='Pinecone API KEY', title='Pinecone API KEY'
    )
    embeddingsProvider: EmbeddingsProvider = Field(
        ...,
        description='Choose the embeddings provider to use for generating embeddings',
        title='Embeddings provider (as defined in the langchain API)',
    )
    embeddingsConfig: Optional[Dict[str, Any]] = Field(
        None,
        description='Specific configuration for the embeddings. For example, for OpenAI, you can the model name as {"model": "text-embedding-ada-002"})',
        title='Embeddings provider configuration',
    )
    embeddingsApiKey: Optional[str] = Field(
        None,
        description='Value of the API KEY for the embeddings provider (if required).\n\n For example for OpenAI it is OPENAI_API_KEY, for Cohere it is COHERE_API_KEY)',
        title='Embeddings API KEY (whenever applicable, depends on provider)',
    )
    datasetFields: List = Field(
        ...,
        description='This array specifies the dataset fields to be selected and stored in the vector store. Only the fields listed here will be included in the vector store.\n\nFor instance, when using the Website Content Crawler, you might choose to include fields such as `text`, `url`, and `metadata.title` in the vector store.',
        title='Dataset fields to select from the dataset results and store in the database',
    )
    datasetFieldsToItemId: Optional[List[str]] = Field(
        ['url'],
        description='This array contains fields that are used to uniquely identify dataset items, which helps to handle content changes across different runs.\n\nFor instance, in a web content crawling scenario, the `url` field could serve as a unique identifier for each item.',
        title='Dateset fields to uniquely identify dataset items',
    )
    metadataDatasetFields: Optional[Dict[str, Any]] = Field(
        None,
        description='A list of dataset fields which should be selected from the dataset and stored as metadata in the vector stores.\n\nFor example, when using the Website Content Crawler, you might want to store `url` in metadata. In this case, use `metadataDatasetFields parameter as follows {"url": "url"}`',
        title='Dataset fields to select from the dataset and store as metadata in the database',
    )
    metadataObject: Optional[Dict[str, Any]] = Field(
        None,
        description='This object allows you to store custom metadata for every item in the vector store.\n\nFor example, if you want to store the `domain` as metadata, use the `metadataObject` like this: {"domain": "apify.com"}.',
        title='Custom object to be stored as metadata in the vector store database',
    )
    enableDeltaUpdates: Optional[bool] = Field(
        True,
        description='When set to true, this setting enables incremental updates for objects in the database by comparing the changes (deltas) between the crawled dataset items and the existing objects, uniquely identified by the `datasetKeysToItemId` field.\n\n The integration will only add new objects and update those that have changed, reducing unnecessary updates. The `datasetFields`, `metadataDatasetFields`, and `metadataObject` fields are used to determine the changes.',
        title='Enable incremental updates for objects based on deltas',
    )
    expiredObjectDeletionPeriod: Optional[int] = Field(
        30,
        description='This setting allows the integration to manage the deletion of objects from the database that have not been crawled for a specified period. It is typically used in subsequent runs after the initial crawl.\n\nWhen the value is greater than 0, the integration checks if objects have been seen within the last X days (determined by the expiration period). If the objects are expired, they are deleted from the database. The specific value for `deletedExpiredObjectsDays` depends on your use case and how frequently you crawl data.\n\nFor example, if you crawl data daily, you can set `deletedExpiredObjectsDays` to 7 days. If you crawl data weekly, you can set `deletedExpiredObjectsDays` to 30 days.',
        ge=0,
        title='Delete expired objects from the database after a specified number of days',
    )
    performChunking: Optional[bool] = Field(
        False,
        description='When set to true, the text will be divided into smaller chunks based on the settings provided below. Proper chunking helps optimize retrieval and ensures accurate and efficient responses.',
        title='Enable text chunking',
    )
    chunkSize: Optional[int] = Field(
        1000,
        description='Defines the maximum number of characters in each text chunk. Choosing the right size balances between detailed context and system performance. Optimal sizes ensure high relevancy and minimal response time.',
        ge=1,
        title='Maximum chunk size',
    )
    chunkOverlap: Optional[int] = Field(
        0,
        description='Specifies the number of overlapping characters between consecutive text chunks. Adjusting this helps maintain context across chunks, which is crucial for accuracy in retrieval-augmented generation systems.',
        ge=0,
        title='Chunk overlap',
    )
    datasetId: Optional[str] = Field(
        None,
        description='Dataset ID (when running standalone without integration)',
        title='Dataset ID',
    )
