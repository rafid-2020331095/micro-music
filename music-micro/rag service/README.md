# RAG Service (LangChain + Qdrant)

🔧 This service demonstrates a simple RAG (retrieval-augmented generation) flow using:
- OpenAI for transcription, embeddings, and LLM responses
- Qdrant (cloud) as the vector store
- LangChain for glue code
- FastAPI as the HTTP API

Features
- Admin endpoint to upload an audio file (song) which will be transcribed, split into 2 chunks, embedded, and stored in Qdrant with `song_id` metadata.
- User endpoint to query about a specific song: the system restricts search to documents with `song_id` and runs similarity search and an LLM answer.

Getting started
1. Copy `.env.example` to `.env` and fill values (OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY).
2. Create a virtualenv and install requirements:

   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

3. Run the app:

   uvicorn app.main:app --reload --port 8001

Endpoints
- POST /admin/upload
  - form fields: `song_id` (string), `title` (optional), `file` (audio file)
  - Action: transcribe -> chunk (2) -> embed -> store

- POST /songs/{song_id}/query
  - json: { "query": "What is the tempo?" }
  - returns: LLM answer using only chunks for that `song_id`.

Notes & Limitations
- This is a minimal, example-grade implementation. Add authentication, background workers, retries, larger chunking logic, and safety checks for production.
- No Redis or Docker used. Qdrant is expected to be a managed cloud instance (provide QDRANT_URL and QDRANT_API_KEY).

Examples
- Upload:
  curl -X POST "http://localhost:8001/admin/upload" -F "song_id=abc123" -F "file=@./song.mp3" -F "title=My Song"

- Query:
  curl -X POST "http://localhost:8001/songs/abc123/query" -H "Content-Type: application/json" -d '{"query":"Tell me about the lyrics"}'

- Process a song (called from your TypeScript admin service after upload):
  curl -X POST "http://localhost:8001/process-song" -H "Content-Type: application/json" -d '{"song_id":"abc123","title":"My Song","audio_url":"https://.../song.mp3"}'

Notes: The recommended architecture is to have your TypeScript `/song/new` endpoint save the song and its audio URL, then POST to `/process-song` with the `audio_url` (no binary file upload). The RAG service will download, transcribe, split into chunks and index into Qdrant.

