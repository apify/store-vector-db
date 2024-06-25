.PHONY: clean install-dev lint type-check check-code format

DIRS_WITH_CODE = code
DIRS_WITH_ACTORS = actors

clean:
	rm -rf .venv .mypy_cache .pytest_cache .ruff_cache __pycache__

install-dev:
	cd $(DIRS_WITH_CODE) && python3 -m pip install --upgrade pip poetry && poetry install --with main,dev,pinecone,chroma,qdrant && poetry run pre-commit install && cd ..

lint:
	poetry run -C $(DIRS_WITH_CODE) ruff check $(DIRS_WITH_CODE)

type-check:
	poetry run -C $(DIRS_WITH_CODE) mypy $(DIRS_WITH_CODE)

check-code: lint type-check

format:
	poetry run -C $(DIRS_WITH_CODE) ruff check --fix $(DIRS_WITH_CODE)
	poetry run -C $(DIRS_WITH_CODE) ruff format $(DIRS_WITH_CODE)

pydantic-model:
	datamodel-codegen --input $(DIRS_WITH_ACTORS)/chroma/.actor/input_schema.json --output $(DIRS_WITH_CODE)/src/models/chroma_input_model.py  --input-file-type jsonschema  --field-constraints
	datamodel-codegen --input $(DIRS_WITH_ACTORS)/pgvector/.actor/input_schema.json --output $(DIRS_WITH_CODE)/src/models/pgvector_input_model.py  --input-file-type jsonschema  --field-constraints
	datamodel-codegen --input $(DIRS_WITH_ACTORS)/pinecone/.actor/input_schema.json --output $(DIRS_WITH_CODE)/src/models/pinecone_input_model.py  --input-file-type jsonschema  --field-constraints
	datamodel-codegen --input $(DIRS_WITH_ACTORS)/qdrant/.actor/input_schema.json --output $(DIRS_WITH_CODE)/src/models/qdrant_input_model.py  --input-file-type jsonschema  --field-constraints

pytest:
	poetry run -C $(DIRS_WITH_CODE) pytest --with-integration --vcr-record=none