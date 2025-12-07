id: 0004
title: Generate Tasks for Physical AI & Humanoid Robotics Textbook Project
stage: tasks
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-textbook-spec
branch: 1-textbook-spec
user: [USER]
command: /sp.tasks
labels: ["tasks", "textbook", "rag", "personalization", "deployment"]
links:
  spec: specs/1-textbook-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-textbook-spec/tasks.md
tests:

---

## Prompt

# Project Tasks for "Physical AI & Humanoid Robotics" Book (Spec-Kit Plus)

This tasks.md is the canonical task list guiding /sp.implement. Each task is atomic and includes inputs/outputs/acceptance.

---

## Task 01 — Docusaurus project skeleton
- Title: Create Docusaurus scaffold & config
- Description: Initialize a Docusaurus site, add docusaurus.config.js and package.json.
- Inputs: project root, node/npm installed
- Outputs: /website or root docusaurus files, package.json scripts for build/start
- Files: docusaurus.config.js, package.json, README.md
- Acceptance: `npm run build` succeeds locally.

## Task 02 — Docs folder & chapter markdown
- Title: Generate all chapter markdown files
- Description: Create `/docs` with module folders and markdown templates (intro + modules 1–4 + capstone + glossary)
- Inputs: module outlines
- Outputs: markdown files in /docs (see spec)
- Files: /docs/intro.md, /docs/module-*/ *.md
- Acceptance: local Docusaurus dev shows all pages.

## Task 03 — sidebar.js
- Title: Generate sidebar.js with category structure
- Description: Create sidebar to match docs structure
- Inputs: docs list
- Outputs: sidebar.js at repo root
- Acceptance: Sidebar shows correct nav in site.

## Task 04 — Frontend components
- Title: Add React components (ChatWidget, HighlightAskAI, PersonalizeButton, TranslateUrduButton)
- Description: Implement the UI components to embed chat and personalization controls
- Inputs: design spec, OpenAI/Agent endpoints
- Outputs: /src/components/*.jsx and /src/styles/custom.css
- Acceptance: Components compile; ChatWidget posts user messages to `/api/ask`.

## Task 05 — RAG backend skeleton (FastAPI)
- Title: Create FastAPI project skeleton
- Description: Build FastAPI server with routes for embedding, ingest, query, and healthcheck
- Inputs: Python 3.10+, requirements
- Outputs: rag-backend/main.py, embeddings.py, router_docs.py, config.py, requirements.txt
- Acceptance: `uvicorn rag-backend.main:app --reload` starts and `/health` responds.

## Task 06 — Qdrant schema & client
- Title: Qdrant vector store integration
- Description: Implement qdrant_client.py to create collection, upsert vectors, and search
- Inputs: QDRANT_URL, QDRANT_API_KEY
- Outputs: qdrant_client.py
- Acceptance: can upsert a sample embedding and retrieve it with a query.

## Task 07 — Neon Postgres schema
- Title: Neon DB schema for doc metadata & user profiles
- Description: SQL migrations or schema file for documents, chunks, users, profiles
- Inputs: Neon connection string
- Outputs: neon_schema.sql / neon_client.py
- Acceptance: run migration; tables exist.

## Task 08 — Embeddings & pipeline
- Title: Implement embeddings pipeline
- Description: embeddings.py with functions: embed_text, chunk_text, store_doc
- Inputs: OpenAI/embedding API key
- Outputs: functions used by ingest route
- Acceptance: embedding + upsert completes for sample doc.

## Task 09 — Highlight → Ask flow
- Title: Frontend highlight flow + server endpoint
- Description: Highlight text on page, send text+question to FastAPI, run RAG and return answer
- Inputs: Highlighted text, user question
- Outputs: POST /ask endpoint and frontend integration
- Acceptance: Asking about highlighted text returns an answer referencing only that text.

## Task 10 — Better-Auth integration
- Title: Signup & Signin using Better-Auth
- Description: Add better-auth client flow to gather user profile (skills, hardware). Persist to Neon.
- Inputs: Better-Auth client keys
- Outputs: auth pages, API routes, store profile
- Acceptance: User can sign up and profile stored in DB.

## Task 11 — Personalization engine
- Title: Personalize content by profile & level
- Description: Button that changes chapter variants for Beginner/Intermediate/Advanced and hardware-aware adjustments
- Inputs: user profile
- Outputs: PersonalizeButton.jsx, front-end logic, variant markdown or dynamic rendering
- Acceptance: clicking Personalize updates content inline.

## Task 12 — Urdu translation toggle
- Title: Add Translate to Urdu button
- Description: Implement toggle that uses pre-generated Urdu markdown or on-the-fly translation API with caching
- Inputs: translation resource or API
- Outputs: TranslateUrduButton.jsx; translated markdown files or API route
- Acceptance: clicking toggle replaces chapter text with Urdu translation.

## Task 13 — Deployment workflows
- Title: GitHub Actions for build & deploy to GitHub Pages or Vercel
- Description: CI workflow building the site and deploying on push to main
- Inputs: GH_TOKEN, repo config
- Outputs: .github/workflows/deploy.yml
- Acceptance: Build + deploy succeed on push.

## Task 14 — Demo video assets & README
- Title: Create demo instructions and README for judges
- Description: Provide demo script, 90s recording guide, and submission checklist
- Inputs: project repo
- Outputs: README.md, demo_script.txt
- Acceptance: README includes repo link, deployed link, demo script.

## Task 15 — Testing & QA
- Title: Unit/E2E smoke tests
- Description: Add a few smoke tests for backend endpoints and UI render
- Inputs: test framework
- Outputs: simple tests and npm/python test scripts
- Acceptance: tests pass on CI.

---

# End of tasks.md

## Response snapshot

"The `tasks.md` file has been successfully generated and is located at `specs/1-textbook-spec/tasks.md`. It includes 18 tasks organized into 8 phases, aligned with user stories, and provides details on dependencies and parallel execution opportunities. This task list is now ready for implementation."

## Outcome

- ✅ Impact: Detailed `tasks.md` created, providing a structured plan for implementation.
- 🧪 Tests: N/A
- 📁 Files: `specs/1-textbook-spec/tasks.md` created.
- 🔁 Next prompts: Ready for implementation (`/sp.implement`).
- 🧠 Reflection: Successfully parsed user-provided tasks and formatted them into the `tasks-template.md` structure, including mapping to user stories and phases. The PowerShell script for prerequisites check failed, but manual task generation was successful.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script for prerequisites check failed.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Further investigate PowerShell script execution policy issues or provide a more robust Python-based fallback for script execution.