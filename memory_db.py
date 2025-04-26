import os
import uuid
from datetime import datetime

from chromadb import PersistentClient
from chromadb.api.models.Collection import IncludeEnum
from chromadb.utils import embedding_functions


class MemoryDB:
    def __init__(self, persist_dir: str = None):
        persist_dir = persist_dir or os.getenv("CHROMA_DB_PERSIST_DIR", "./chroma_db")

        self.client = PersistentClient(
            path=persist_dir
        )

        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-ada-002"
        )

        self.collection = self.client.get_or_create_collection(
            name="memory",
            embedding_function=self.embedding_function
        )

    def save(self, role: str, content: str):
        id_ = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        self.collection.add(
            ids=[id_],
            documents=[content],
            metadatas=[{"role": role, "timestamp": timestamp}]
        )

    def smart_search(self, query: str, limit: int = 5):
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            include=[IncludeEnum.metadatas, IncludeEnum.documents]
        )
        found = []
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        for doc, meta in zip(docs, metas):
            found.append({
                "role": meta.get("role"),
                "content": doc,
                "timestamp": meta.get("timestamp")
            })
        return found
