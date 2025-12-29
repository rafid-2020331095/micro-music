

import os
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from tempfile import NamedTemporaryFile
import httpx
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient,models
from qdrant_client.http.models import Distance, VectorParams
import openai
from openai import OpenAI
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

# ✅ Create payload index for song_id (integer)
try:
    qdrant_client.create_payload_index(
        collection_name=QDRANT_COLLECTION,
        field_name="song_id",
        field_schema=models.IntegerIndexParams(
            type=models.IntegerIndexType.INTEGER,
            lookup=True,
            range=True
        )
    )
except Exception as e:
    print("Payload index already exists or error:", e)
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=QDRANT_COLLECTION,
    embedding=embeddings,
)

# ===============================
# HELPER FUNCTIONS
# ===============================

def transcribe_file(file_path: str) -> str:
    """
    Blocking Whisper call (runs in background thread)
    """
    with open(file_path, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
        )
        
    clienta = OpenAI()

    romanized = clienta.responses.create(
        model="gpt-4.1-mini",
        input=f"Transliterate this Hindi text into Roman English:\n\n{transcript.text}"
    )

    print(romanized.output_text)
    return romanized.output_text


async def download_audio(audio_url: str) -> str:
    """
    Download audio file asynchronously
    """
    suffix = os.path.splitext(audio_url)[1] or ".mp3"

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.get(audio_url)
        response.raise_for_status()

        with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(response.content)
            return tmp.name


# ===============================
# BACKGROUND JOB
# ===============================

def process_song_job(payload: dict):
    """
    Runs AFTER response is returned
    """

    tmp_path = None

    try:
        song_id = payload["song_id"]
        title = payload.get("title", "")
        audio_url = payload["audio_url"]

        # 1️⃣ Download (run async code safely)
        tmp_path = asyncio.run(download_audio(audio_url))

        # 2️⃣ Transcribe
        transcript = transcribe_file(tmp_path)

        if not transcript:
            raise RuntimeError("Empty transcription")

        # 3️⃣ Create document
        doc = Document(
            page_content=transcript,
            metadata={
                "song_id": song_id,
                "title": title,
                "type": "song",
            },
        )

        # 4️⃣ Chunk
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=100,
        )
        chunks = splitter.split_documents([doc])

        # 5️⃣ Store in Qdrant
        vector_store.add_documents(chunks)

        print(f"[SUCCESS] Indexed song {song_id} with {len(chunks)} chunks")

    except Exception as e:
        print(f"[ERROR] Failed processing song: {e}")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


# ===============================
# API ENDPOINT (FAST RESPONSE)
# ===============================

@router.post("/process-song", status_code=202)
async def process_song(payload: dict, background_tasks: BackgroundTasks):
    """
    Fire-and-forget ingestion endpoint
    """

    if "song_id" not in payload or "audio_url" not in payload:
        raise HTTPException(
            status_code=400,
            detail="song_id and audio_url are required",
        )

    # 🚀 Background execution
    background_tasks.add_task(process_song_job, payload)

    # ⚡ Immediate response
    return {
        "status": "accepted",
        "message": "Song processing started",
        "song_id": payload["song_id"],
    }
