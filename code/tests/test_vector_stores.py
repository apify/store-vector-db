from __future__ import annotations

import time
from typing import TYPE_CHECKING

import pytest

from src.constants import VCR_HEADERS_EXCLUDE
from src.vcs import compare_crawled_data_with_db, update_db_with_crawled_data

from .conftest import ID1, ID3, ID4A, ID4B, ID4C, ID5A, ID5B, ID5C, ID6

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from langchain_core.documents import Document

    from src._types import VectorDb

# Database fixtures to test. Fill here the name of the fixtures you want to test
DATABASE_FIXTURES = ["db_pinecone", "db_chroma", "db_qdrant"]


def wait_for_db(sec: int = 3) -> None:
    # Wait for the database to update (Pinecone)
    # Data freshness - Pinecone is eventually consistent, so there can be a slight delay before new or changed records are visible to queries.
    time.sleep(sec)


@pytest.mark.integration()
@pytest.mark.vcr(filter_headers=VCR_HEADERS_EXCLUDE)
@pytest.mark.parametrize("input_db", DATABASE_FIXTURES)
def test_add_newly_crawled_data(input_db: str, crawl_2: list[Document], request: FixtureRequest) -> None:
    db: VectorDb = request.getfixturevalue(input_db)

    res = db.search_by_vector(db.dummy_vector, k=10)
    assert len(res) == 6, "Expected 6 initial objects in the database"

    data_add, _, _ = compare_crawled_data_with_db(db, crawl_2)

    assert len(data_add) == 4, "Expected 4 objects to add"
    assert data_add[0].metadata["id"] == ID4C
    assert data_add[1].metadata["id"] == ID5B
    assert data_add[2].metadata["id"] == ID5C
    assert data_add[3].metadata["id"] == ID6

    # Add new data
    db.add_documents(data_add, ids=[d.metadata["id"] for d in data_add])
    wait_for_db(db.unit_test_wait_for_index)

    res = db.search_by_vector(db.dummy_vector, k=10)
    ids = [r.metadata["id"] for r in res]
    assert len(res) == 10, "Expected 10 objects in the database after addition"
    assert ID4C in ids, f"Expected {ID4C} to be added"
    assert ID5B in ids, f"Expected {ID5B} to be added"
    assert ID5C in ids, f"Expected {ID5C} to be added"


@pytest.mark.integration()
@pytest.mark.vcr(filter_headers=VCR_HEADERS_EXCLUDE)
@pytest.mark.parametrize("input_db", DATABASE_FIXTURES)
def test_update_metadata_last_seen_at(input_db: str, crawl_2: list[Document], request: FixtureRequest) -> None:
    db: VectorDb = request.getfixturevalue(input_db)

    res = db.search_by_vector(db.dummy_vector, k=10)
    assert len(res) == 6, "Expected 6 initial objects in the database"

    _, ids_update_last_seen, _ = compare_crawled_data_with_db(db, crawl_2)

    assert len(ids_update_last_seen) == 1, "Expected 1 object to update"
    assert ID3 in ids_update_last_seen, f"Expected {ID3} to be updated"

    res = db.search_by_vector(db.dummy_vector, k=10)
    assert next(r for r in res if r.metadata["id"] == ID3).metadata["last_seen_at"] == 1

    # Update metadata data
    db.update_last_seen_at(ids_update_last_seen)
    wait_for_db(db.unit_test_wait_for_index)

    res = db.search_by_vector(db.dummy_vector, k=10)
    assert len(res) == 6, "Expected 6 objects in the database after last_seen update"
    assert next(r for r in res if r.metadata["id"] == ID3).metadata["last_seen_at"] > 1, f"Expected {ID3} to be updated"


@pytest.mark.parametrize("input_db", DATABASE_FIXTURES)
def test_delete_updated_data(input_db: str, crawl_2: list[Document], request: FixtureRequest) -> None:
    db: VectorDb = request.getfixturevalue(input_db)

    res = db.search_by_vector(db.dummy_vector, k=10)
    assert len(res) == 6, "Expected 6 initial objects in the database"

    _, _, ids_del = compare_crawled_data_with_db(db, crawl_2)

    assert len(ids_del) == 3, "Expected 1 object to delete"
    assert ID4A in ids_del, f"Expected {ID4A} to be deleted"
    assert ID4B in ids_del, f"Expected {ID4B} to be deleted"
    assert ID5A in ids_del, f"Expected {ID5A} to be deleted"

    db.delete(ids=ids_del)
    wait_for_db(db.unit_test_wait_for_index)

    res = db.search_by_vector(db.dummy_vector, k=10)
    ids = [r.metadata["id"] for r in res]
    assert len(ids) == 3, "Expected 3 objects in the database after deletion"
    assert ID4A not in ids, f"Expected {ID4A} to be deleted"
    assert ID4B not in ids, f"Expected {ID4B} to be deleted"
    assert ID5A not in ids, f"Expected {ID5A} to be deleted"


@pytest.mark.integration()
@pytest.mark.vcr(filter_headers=VCR_HEADERS_EXCLUDE)
@pytest.mark.parametrize("input_db", DATABASE_FIXTURES)
def test_deleted_expired_data(input_db: str, request: FixtureRequest) -> None:
    db: VectorDb = request.getfixturevalue(input_db)
    res = db.search_by_vector(db.dummy_vector, k=10)
    assert len(res) == 6, "Expected 6 initial objects in the database"

    # Delete expired objects
    db.delete_expired(expired_ts=1)
    wait_for_db(db.unit_test_wait_for_index)

    res = db.search_by_vector(db.dummy_vector, k=10)
    assert len(res) == 5, "Expected 5 objects in the database after deletion"
    assert ID1 not in [r.metadata["id"] for r in res], f"Expected {ID1} to be deleted"


@pytest.mark.integration()
@pytest.mark.vcr(filter_headers=VCR_HEADERS_EXCLUDE)
@pytest.mark.parametrize("input_db", DATABASE_FIXTURES)
def test_update_db_with_crawled_data_all(input_db: str, crawl_2: list[Document], expected_results: list[Document], request: FixtureRequest) -> None:
    db: VectorDb = request.getfixturevalue(input_db)

    res = db.search_by_vector(db.dummy_vector, k=10)
    assert len(res) == 6, "Expected 6 initial objects in the database"

    update_db_with_crawled_data(db, crawl_2, 1)
    wait_for_db(db.unit_test_wait_for_index)

    res = db.search_by_vector(db.dummy_vector, k=10)
    assert len(res) == 6, "Expected 6 objects in the database after all updates"

    # Compare results with expected results
    for expected in expected_results:
        d = next(r for r in res if expected.metadata["id"] == r.metadata["id"])
        assert d.metadata["item_id"] == expected.metadata["item_id"], f"Expected item_id {expected.metadata['item_id']}"
        assert d.metadata["checksum"] == expected.metadata["checksum"], f"Expected checksum {expected.metadata['checksum']}"
