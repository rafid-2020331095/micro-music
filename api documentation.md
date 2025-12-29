# API Documentation ✅

> Overview: This project contains three microservices under `music-micro`: **User Service**, **Admin Service**, and **Song Service**. Each service mounts routes under `/api/v1` (e.g., `http://localhost:<PORT>/api/v1/...`).

---

## Common notes 🔧

- Authentication: Protected endpoints require a JWT token passed in the request header named `token` (e.g., `token: <JWT>`).
- File uploads: Use `multipart/form-data` and include the file in the `file` field.
- Content-Type: Use `application/json` for JSON payloads and `multipart/form-data` for file uploads.

---

## User Service (default port: `5000`) 📁
Base path: `http://localhost:5000/api/v1`

| Method | URL | Auth | Input (example) | Success response |
|---|---:|:---:|---|---|
| POST | `/user/register` | No | JSON: `{ "name": "Alice", "email": "a@x.com", "password": "secret" }` | 201 `{ message: "User Registered", user: {...}, token: "..." }` |
| POST | `/user/login` | No | JSON: `{ "email": "a@x.com", "password": "secret" }` | 200 `{ message: "Logged IN", user: {...}, token: "..." }` |
| GET | `/user/me` | Yes (`token` header) | — | 200 `user` object (no password field) |
| POST | `/song/:id` | Yes (`token` header) | URL param: `id` (song id) | 200 `{ message: "Added to PlayList" }` or `{ message: " Removed from playlist" }` |

---

## Admin Service 📁
Base path: `http://localhost:<PORT>/api/v1` (set via `PORT` env var)

> All admin endpoints require authentication via header `token` and **user role must be `admin`**.

| Method | URL | Auth | Input (example) | Success response |
|---|---:|:---:|---|---|
| POST | `/album/new` | Yes (admin) | Multipart form-data: fields `title`, `description`, `file` (album thumbnail) | 200 `{ message: "Album Created", album: {...} }` |
| POST | `/song/new` | Yes (admin) | Multipart form-data: `title`, `description`, `album` (album id), `file` (audio) | 200 `{ message: "Song Added" }` |
| POST | `/song/:id` | Yes (admin) | URL param: `id`, multipart form-data: `file` (thumbnail) | 200 `{ message: "Thumbnail added", song: {...} }` |
| DELETE | `/album/:id` | Yes (admin) | URL param: `id` | 200 `{ message: "Album deleted successfully" }` |
| DELETE | `/song/:id` | Yes (admin) | URL param: `id` | 200 `{ message: "Song deleted successfully" }` |

Notes:
- Upload field name for files is `file` (see `multer` usage).

---

## Song Service 📁
Base path: `http://localhost:<PORT>/api/v1` (set via `PORT` env var)

| Method | URL | Auth | Input | Success response |
|---|---:|:---:|---|---|
| GET | `/album/all` | No | — | 200 `[{ id, title, description, thumbnail, created_at }, ...]` |
| GET | `/song/all` | No | — | 200 `[{ id, title, description, thumbnail, audio, album_id, created_at }, ...]` |
| GET | `/album/:id` | No | URL param: `id` | 200 `{ songs: [...], album: {...} }` or 404 `{ message: "No album with this id" }` |
| GET | `/song/:id` | No | URL param: `id` | 200 `song` object (or `undefined` if not found) |

---

## Authentication example 💡

Header:
```
token: <JWT token string>
```

Example curl for protected endpoint (user profile):
```
curl -H "token: <JWT>" http://localhost:5000/api/v1/user/me
```

Example curl for album upload (admin):
```
curl -X POST -H "token: <JWT>" -F "title=My Album" -F "description=..." -F "file=@cover.jpg" http://localhost:4000/api/v1/album/new
```

---

If you'd like, I can:
- Add examples with sample responses for each endpoint ✅
- Generate a Postman collection or OpenAPI (Swagger) spec 🔧

---

*Generated from route definitions and controller logic in the repository.*
