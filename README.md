# My Music App 🎵

**Short description:** A full-stack music application consisting of a Vite + React frontend and a set of TypeScript microservices (admin, song, user). This repository stores the frontend and a `music-micro` folder with three microservices that provide the backend API.

---

## Table of contents

- [Project overview](#project-overview)
- [Architecture](#architecture)
- [Folder structure & file descriptions](#folder-structure--file-descriptions)
  - [Frontend](#frontend)
  - [microservices (music-micro)](#microservices-music-micro)
- [Setup & Run (development)](#setup--run-development)
  - [Frontend](#frontend-1)
  - [Microservices](#microservices)
- [Environment variables & config](#environment-variables--config)
- [API & routes (summary)](#api--routes-summary)
- [Notes for contributors](#notes-for-contributors)
- [License](#license)

---

## Project overview

This project implements a music streaming-like web application where users can sign up / sign in, browse albums and playlists, and play songs. The frontend is implemented in React + TypeScript (Vite), and the backend is separated into microservices under `music-micro/`:

- `admin service` — admin endpoints and utilities
- `song service` — CRUD and query endpoints for songs and albums
- `user service` — user registration, login, and user-related endpoints

Each backend service is implemented in TypeScript and follows a similar structure (controllers, routes, middleware, and configuration files).

---

## Architecture

- Client (React + Vite) interacts with microservices over REST APIs.
- Services are independent Node/TypeScript apps (single responsibility for users, songs, admin tasks).
- Shared patterns:
  - `controller.ts` — request handlers
  - `route.ts` — express routes & endpoint wiring
  - `middleware.ts` — authentication, validation, or request handling middlewares
  - `TryCatch.ts` — an async wrapper for handling promise rejections / errors centrally
  - `config/` — DB and environment configuration

---

## Folder structure & file descriptions

Below is a concise description of each notable folder/file in the repository. Use it as a reference when working on or extending the project.

### Frontend (folder: `frontend/`)

- `package.json` — project metadata and NPM scripts (install, dev, build, etc.).
- `vite.config.ts` — Vite configuration for the React app.
- `index.html` — main HTML entry.
- `src/main.tsx` — React entry point that mounts the app.
- `src/App.tsx` — root React component and application-level layout.
- `src/index.css` — global styles.

#### Components (in `src/components/`)
- `Navbar.tsx` — top navigation and links.
- `Sidebar.tsx` — side navigation (e.g., playlists, libraries).
- `Player.tsx` — audio player controls (play/pause, seek, next, prev).
- `Loading.tsx` — loading indicator component for async states.
- `AlbumCard.tsx` — UI card to display album information.
- `SongCard.tsx` — UI card to display a single song entry.
- `PlayListCard.tsx` — UI card to display playlists.

#### Contexts (in `src/context/`)
- `UserContext.tsx` — React context for user authentication state and functions.
- `SongContext.tsx` — React context for currently playing song, playlist, and player controls.

#### Pages (in `src/pages/`)
- `Home.tsx` — landing/dashboard page showcasing songs, albums, and playlists.
- `Login.tsx` — login form and auth flow.
- `Register.tsx` — user registration form.
- `Album.tsx` — album details view and list of songs.
- `PlayList.tsx` — playlist view and management.
- `Admin.tsx` — admin-only UI for managing songs, albums, or users (if applicable).

---

### Microservices (folder: `music-micro/`)

Each service has a similar layout and purpose. The three services are placed under `music-micro/`.

General files present in each service's `src/` directory:

- `index.ts` — service entry point; starts the Express server and uses `route.ts` to load routes.
- `controller.ts` — contains handlers for endpoints (CRUD operations, business logic).
- `route.ts` — defines and exports express Router with endpoints mapped to controllers.
- `middleware.ts` — middleware functions (e.g., auth checks, validation) — note: some services may not have `middleware.ts` if not needed.
- `TryCatch.ts` — helper to wrap async controller functions to handle rejections and forward errors to error handlers.
- `config/db.ts` — database connection helper, e.g., function that connects to MongoDB or other DB.
- `config/dataUri.ts` — in `admin service`, likely used to parse or store data URIs for media (images/audio) or other constants.

Service-specific notes:

#### Admin service (`admin service/`)
- Purpose: administrative tasks, possibly uploading assets, seeding data, or performing moderation actions. Contains `dataUri.ts` and other admin-specific utilities.

#### Song service (`song service/`)
- Purpose: manage song resources (create, read, update, delete), query by album/artist, serve metadata for the frontend.

#### User service (`user service/`)
- Purpose: registration, login, user profile, and authorization-related endpoints.
- `model.ts` — user schema/model (if using a DB like MongoDB + Mongoose or another ORM). This file defines the user data shape and validation.

---

## Setup & Run (development)

> Notes: exact scripts are defined in each `package.json`. Use `npm run` to see available scripts.

### Frontend

1. Open a terminal and go to the frontend folder:

```bash
cd frontend
npm install
npm run dev
```

Common scripts you can expect:
- `npm run dev` — start Vite dev server (hot reload)
- `npm run build` — build production bundle
- `npm run preview` — preview the production build

### Microservices (for each service)

1. Open a terminal and change directory into a service folder, for example `user service`:

```bash
cd music-micro/user\ service
npm install
npm run dev
# or
npm start
```

Common dev workflow:
- `npm run dev` — start the service in watch mode (using nodemon / ts-node-dev)
- `npm start` — start the production server (compiled JS via node)

Make sure each service has the required environment variables set and that the database (if any) is running and accessible.

---

## Environment variables & config

Each back-end service will typically need:
- `PORT` — port to run the Express server
- `DATABASE_URI` / `MONGO_URI` — DB connection string
- `JWT_SECRET` — for token signing (if authentication is JWT-based)
- Any cloud or file storage credentials if uploads are supported

Look inside each service's `config/` folder and the `index.ts` files to see exactly which environment variables the service expects.

---

## API & routes (summary)

- `user service` — endpoints for user registration and authentication (e.g., POST `/auth/register`, POST `/auth/login`, GET `/me`).
- `song service` — endpoints for retrieving and managing songs and albums (e.g., GET `/songs`, POST `/songs`, GET `/albums/:id`).
- `admin service` — administrative endpoints (seeding, uploading, moderation).

Check each service's `route.ts` for the precise endpoints and request/response schemas.

---

## Notes for contributors 🔧

- Follow the existing TypeScript and folder conventions when adding features.
- Use `TryCatch` wrapper for async controllers to centralize error handling.
- Keep services small and focused — add new endpoints into the relevant microservice.
- Add or update tests where applicable (not included by default in this repo snapshot).

---

## Troubleshooting & tips 💡

- If the frontend cannot reach APIs, confirm each service is running and the frontend uses the correct base URL (check `.env` or `src` config).
- To quickly restart a service on code changes, use `npm run dev` (watch mode) or ensure a `nodemon`/`ts-node-dev` script exists.

---

## License & contact

- Add your preferred LICENSE file to the repository (e.g., `MIT`) and update this section accordingly.
- Questions / Issues: open an issue describing the problem or desired feature.

---

If you want, I can:
- Add more detailed endpoint documentation (example requests/responses) by reading `route.ts` and `controller.ts` files, or
- Create a top-level `README` at the workspace root with quick-start scripts and a diagram.

---

*Generated on Dec 23, 2025*