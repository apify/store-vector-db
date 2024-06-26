from __future__ import annotations

import os
import time

import pytest
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from models import ChromaIntegration, PgvectorIntegration, PineconeIntegration, QdrantIntegration  # type: ignore[import]
from models.pinecone_input_model import EmbeddingsProvider  # type: ignore[import]
from utils import add_item_checksum  # type: ignore[import]
from vector_stores.chroma import ChromaDatabase  # type: ignore[import]
from vector_stores.pgvector import PGVectorDatabase  # type: ignore[import]
from vector_stores.pinecone import PineconeDatabase  # type: ignore[import]
from vector_stores.qdrant import QdrantDatabase  # type: ignore[import]

load_dotenv()
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

INDEX_NAME = "apify-unit-test"

UUID = "00000000-0000-0000-0000-0000000000"
ID1 = f"{UUID}10"
ID2 = f"{UUID}20"
ID3 = f"{UUID}30"
ID4A, ID4B, ID4C = f"{UUID}4a", f"{UUID}4b", f"{UUID}4c"
ID5A, ID5B, ID5C = f"{UUID}5a", f"{UUID}5b", f"{UUID}5c"
ID6 = f"{UUID}60"

ITEM_ID1 = "id1"
ITEM_ID4 = "id4"

d1 = Document(page_content="Expired->del", metadata={"item_id": ITEM_ID1, "chunk_id": ID1, "checksum": "1", "last_seen_at": 0})
d2 = Document(page_content="Old->not-del", metadata={"item_id": "id2", "chunk_id": ID2, "checksum": "2", "last_seen_at": 1})
d3a = Document(page_content="Unchanged->upt-meta", metadata={"item_id": "id3", "chunk_id": ID3, "checksum": "3", "last_seen_at": 1})
d3b = Document(page_content="Unchanged->upt-meta", metadata={"item_id": "id3", "chunk_id": ID3, "checksum": "3", "last_seen_at": 2})
d4a = Document(page_content="Changed->del", metadata={"item_id": ITEM_ID4, "chunk_id": ID4A, "checksum": "4", "last_seen_at": 1})
d4b = Document(page_content="Changed->del", metadata={"item_id": ITEM_ID4, "chunk_id": ID4B, "checksum": "4", "last_seen_at": 1})
d4c = Document(page_content="Changed->add-new", metadata={"item_id": ITEM_ID4, "chunk_id": ID4C, "checksum": "4c", "last_seen_at": 2})
d5a = Document(page_content="Changed->del", metadata={"item_id": "id5", "chunk_id": ID5A, "checksum": "5", "last_seen_at": 1})
d5b = Document(page_content="Changed->add-new", metadata={"item_id": "id5", "chunk_id": ID5B, "checksum": "5bc", "last_seen_at": 2})
d5c = Document(page_content="Changed->add-new", metadata={"item_id": "id5", "chunk_id": ID5C, "checksum": "5bc", "last_seen_at": 2})
d6 = Document(page_content="New->add", metadata={"item_id": "id5", "chunk_id": ID6, "checksum": "6", "last_seen_at": 2})


@pytest.fixture()
def crawl_1() -> list[Document]:
    return [d1, d2, d3a, d4a, d4b, d5a]


@pytest.fixture()
def crawl_2() -> list[Document]:
    return [d3b, d4c, d5b, d5c, d6]


@pytest.fixture()
def expected_results() -> list[Document]:
    return [d2, d3b, d4c, d5b, d5c, d6]


@pytest.fixture()
def documents() -> list[Document]:
    d = Document(page_content="Content", metadata={"url": "https://url1.com"})
    return add_item_checksum([d], ["url"])


@pytest.fixture()
def db_pinecone(crawl_1: list[Document]) -> PineconeDatabase:
    db = PineconeDatabase(
        actor_input=PineconeIntegration(
            pineconeIndexName=INDEX_NAME,
            pineconeApiKey=os.getenv("PINECONE_API_KEY"),
            embeddingsProvider=EmbeddingsProvider.OpenAI,
            embeddingsApiKey=os.getenv("OPENAI_API_KEY"),
            datasetFields=["text"],
        ),
        embeddings=embeddings,
    )
    # Data freshness - Pinecone is eventually consistent, so there can be a slight delay before new or changed records are visible to queries.
    db.unit_test_wait_for_index = 10

    db.delete_all()
    # Insert initially crawled objects
    db.add_documents(documents=crawl_1, ids=[d.metadata["chunk_id"] for d in crawl_1])
    time.sleep(db.unit_test_wait_for_index)

    yield db

    db.delete_all()
    time.sleep(db.unit_test_wait_for_index)


@pytest.fixture()
def db_chroma(crawl_1: list[Document]) -> ChromaDatabase:
    db = ChromaDatabase(
        actor_input=ChromaIntegration(
            chromaClientHost=os.getenv("CHROMA_CLIENT_HOST"),
            embeddingsProvider=EmbeddingsProvider.OpenAI.value,
            embeddingsApiKey=os.getenv("OPENAI_API_KEY"),
            datasetFields=["text"],
            chromaCollectionName=INDEX_NAME,
        ),
        embeddings=embeddings,
    )

    db.unit_test_wait_for_index = 0

    db.delete_all()
    # Insert initially crawled objects
    db.add_documents(documents=crawl_1, ids=[d.metadata["chunk_id"] for d in crawl_1])

    yield db

    db.delete_all()


@pytest.fixture()
def db_qdrant(crawl_1: list[Document]) -> QdrantDatabase:
    db = QdrantDatabase(
        actor_input=QdrantIntegration(
            qdrantUrl=os.getenv("QDRANT_URL"),
            qdrantCollectionName=INDEX_NAME,
            embeddingsProvider=EmbeddingsProvider.OpenAI.value,
            embeddingsApiKey=os.getenv("OPENAI_API_KEY"),
            datasetFields=["text"],
        ),
        embeddings=embeddings,
    )

    db.unit_test_wait_for_index = 0

    db.delete_all()
    # Insert initially crawled objects
    db.add_documents(documents=crawl_1, ids=[d.metadata["chunk_id"] for d in crawl_1])

    yield db

    db.delete_all()


@pytest.fixture()
def db_pgvector(crawl_1: list[Document]) -> PGVectorDatabase:
    db = PGVectorDatabase(
        actor_input=PgvectorIntegration(
            postgresSqlConnectionStr=os.getenv("POSTGRESQL_CONNECTION_STR"),
            postgresCollectionName=INDEX_NAME,
            embeddingsProvider=EmbeddingsProvider.OpenAI.value,
            embeddingsApiKey=os.getenv("OPENAI_API_KEY"),
            datasetFields=["text"],
        ),
        embeddings=embeddings,
    )

    db.unit_test_wait_for_index = 0

    db.delete_all()
    # Insert initially crawled objects
    db.add_documents(documents=crawl_1, ids=[d.metadata["chunk_id"] for d in crawl_1])

    yield db

    db.delete_all()
