import sys
from functools import partial

from apify import Actor

from .models.chroma_input_model import ChromaIntegration
from .models.pinecone_input_model import PineconeIntegration

TypeDb = ChromaIntegration | PineconeIntegration


async def get_database(aid: TypeDb) -> partial:  # type: ignore
    """Get database based on the integration type."""

    if isinstance(aid, ChromaIntegration):

        # Apify dockerfile is using Debian slim-buster image, which has an unsupported version of sqlite3.
        # FIx for RuntimeError: Your system has an unsupported version of sqlite3. Chroma requires sqlite3 >= 3.35.0.
        # References:
        #  https://docs.trychroma.com/troubleshooting#sqlite
        #  https://gist.github.com/defulmere/8b9695e415a44271061cc8e272f3c300
        #
        # pip install pysqlite3
        # swap the stdlib sqlite3 lib with the pysqlite3 package, before importing chromadb
        __import__("pysqlite3")
        sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

        import chromadb
        from langchain_chroma import Chroma

        settings = None
        if auth := aid.chroma_server_auth_credentials:
            settings = chromadb.config.Settings(
                chroma_client_auth_credentials=auth,
                chroma_client_auth_provider="chromadb.auth.token.TokenAuthClientProvider",
            )

        try:
            chroma_client = chromadb.HttpClient(
                host=aid.chroma_client_host,
                port=aid.chroma_client_port or 8000,
                ssl=aid.chroma_client_ssl or False,
                settings=settings,
            )
            assert chroma_client.heartbeat() > 1
            Actor.log.debug("Connected to chroma database")
            return partial(Chroma.from_documents, client=chroma_client, collection_name=aid.chroma_collection_name)
        except Exception as e:
            await Actor.fail(status_message=f"Failed to connect to chroma: {e}")

    if isinstance(aid, PineconeIntegration):

        from langchain_pinecone import PineconeVectorStore

        try:
            return partial(PineconeVectorStore.from_documents, index_name=aid.pinecone_api_key)
        except Exception as e:
            await Actor.fail(status_message=f"Failed to initialize pinecone: {e}")

    await Actor.fail(status_message=f"Failed to get database with config: {aid}")