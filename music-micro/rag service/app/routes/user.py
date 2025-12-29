

from fastapi import APIRouter, HTTPException
from ..schemas import QueryRequest, QueryResponse
from langchain.messages import SystemMessage, HumanMessage
from qdrant_client import models
from langchain.chat_models import init_chat_model
import os
from fastapi import APIRouter, HTTPException
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import openai
# from openai import OpenAI
router = APIRouter()

# ===============================
# CONFIG
# ===============================

openai.api_key = os.getenv("OPENAI_API_KEY")

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "songs")

# ===============================
# QDRANT + EMBEDDINGS (GLOBAL)
# ===============================

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

qdrant_client = QdrantClient(
    url="https://4823d84b-80da-4f60-9d00-b25e674a1a5c.europe-west3-0.gcp.cloud.qdrant.io",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.BbK-9hr7tZrBDyAALDuN9BrUIh5EngbNXvd58SX0ywI",
    prefer_grpc=False,
)

# Ensure collection exists (run once at startup)
if not qdrant_client.collection_exists(QDRANT_COLLECTION):
    qdrant_client.create_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(
            size=3072,
            distance=Distance.COSINE,
        ),
    )

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=QDRANT_COLLECTION,
    embedding=embeddings,
)
router = APIRouter()


llm = init_chat_model("gpt-4o-mini")


# @router.post("/songs/{song_id}/query", response_model=QueryResponse)
# async def query_song(song_id: str, body: QueryRequest):
#     """
#     Query a single song using RAG.
#     Retrieval is strictly limited to chunks with the given song_id.
#     """

#     # ✅ Qdrant-compatible filter
#     qdrant_filter = models.Filter(
#         must=[
#             models.FieldCondition(
#                 key="song_id",
#                 match=models.MatchValue(value=int(song_id)),
#             )
#         ]
#     )

#     # 1️⃣ Song-scoped semantic retrieval (CORRECT)
#     docs = vector_store.similarity_search(
#         query=body.query,
#         k=2,
#         filter=qdrant_filter
#     )

#     if not docs:
#         raise HTTPException(
#             status_code=404,
#             detail="No relevant information found for this song or there is some othere problem"
#         )

#     # 2️⃣ Serialize retrieved chunks
#     context = "\n\n".join(
#         f"Chunk {doc.metadata.get('chunk_index')}:\n{doc.page_content}"
#         for doc in docs
#     )
#     # 3️⃣ Strict grounding prompt (doc-style)
#     messages = [
#         SystemMessage(
#             "You are a helpful assistant answering questions about song lyrics. "
#             "Use ONLY the provided context. "
#             "If the answer is not in the context, say 'I don't know.'"
#         ),
#         HumanMessage(
#             f"Context:\n{context}\n\nQuestion:\n{body.query}"
#         )
#     ]

#     # 4️⃣ LLM call
#     response = llm.invoke(messages)

#     # 5️⃣ API response
#     return QueryResponse(
#         answer=response.content.strip(),
#         source_chunks=[doc.metadata for doc in docs]
#     )

@router.post("/songs/query", response_model=QueryResponse)
async def query_song(body: QueryRequest):
    """
    Query all songs using RAG.
    Retrieval is based purely on vector similarity (no song_id filter).
    """

    # 1️⃣ Vector similarity search
    docs = vector_store.similarity_search(
        query=body.query,
        k=5  # you can increase k to get more chunks
    )

    if not docs:
        raise HTTPException(
            status_code=404,
            detail="No relevant information found."
        )

    # 2️⃣ Serialize retrieved chunks
    context = "\n\n".join(
        f"Chunk {doc.metadata.get('chunk_index')}:\n{doc.page_content}"
        for doc in docs
    )

    # 3️⃣ Strict grounding prompt
    messages = [
        SystemMessage(
            "You are a helpful assistant answering questions about song lyrics. "
        ),
        HumanMessage(
            f"Context:\n{context}\n\nQuestion:\n{body.query}"
        )
    ]

    # 4️⃣ LLM call
    response = llm.invoke(messages)

    # 5️⃣ Return API response
    return QueryResponse(
        answer=response.content.strip(),
        source_chunks=[doc.metadata for doc in docs]
    )
