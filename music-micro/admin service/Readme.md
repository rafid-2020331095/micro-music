copy the tsconfig.json from user service
npm init -y
npm i express dotenv cloudinary redis
npm i @types/express @types/dotenv @neondatabase/serverless  @types/redis cors @types/cors
npm i -D nodemon concurrently typescript
npm i multer datauri
tsc ->vey imp before running npm run dev for the first time.
npm run dev


Integration with RAG service
- After a successful `/song/new` upload, the admin service will POST to the Python RAG service to trigger transcription and indexing.
- Set the environment variable `RAG_SERVICE_URL` (default: `http://localhost:8001`) to point at the RAG service.

Example env entry:
RAG_SERVICE_URL=http://localhost:8001
