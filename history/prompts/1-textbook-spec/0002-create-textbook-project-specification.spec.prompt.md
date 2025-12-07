id: 0002
title: Create Textbook Project Specification
stage: spec
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-textbook-spec
branch: master
user: [USER]
command: /sp.specify
labels: ["spec", "textbook", "rag", "personalization"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-textbook-spec/spec.md
  - specs/1-textbook-spec/checklists/requirements.md
tests:

---

## Prompt

Create a detailed specification for the full Physical AI & Humanoid Robotics textbook project.

Include:

1. Docusaurus project structure
2. Folder structure
3. Chapter list for every module (1–4 + Capstone)
4. All required content sections
5. All required diagrams (as TODO placeholders)
6. RAG chatbot architecture:
   - FastAPI
   - Neon Postgres schema
   - Qdrant schema
   - Text embed + query flow
   - API routes
7. Frontend integration:
   - Chat widget
   - Highlight text → Ask AI
8. Better-Auth integration details:
   - Sign up flow
   - Profile collection (skills + hardware)
9. Personalization engine:
   - Level: Beginner / Intermediate / Advanced
   - Hardware-based content variation
10. Urdu translation button mechanism
11. Build + deploy instructions:
   - GitHub Pages
   - Vercel option
12. Final submission requirements:
   - GitHub repo
   - Deployed link
   - 90-second demo video

## Response snapshot

The detailed specification for the "Physical AI & Humanoid Robotics Textbook Project" has been created at `specs/1-textbook-spec/spec.md`, along with a quality checklist at `specs/1-textbook-spec/checklists/requirements.md`.

## Outcome

- ✅ Impact: Detailed specification created and validated.
- 🧪 Tests: N/A
- 📁 Files: `specs/1-textbook-spec/spec.md` and `specs/1-textbook-spec/checklists/requirements.md` created.
- 🔁 Next prompts: Ready for planning (`/sp.plan`).
- 🧠 Reflection: PowerShell script for feature creation failed due to execution policy, requiring manual directory and file creation.

## Evaluation notes (flywheel)

- Failure modes observed: PowerShell script for feature creation failed, requiring agent-native fallback for directory and file creation.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Address PowerShell execution policy issues or provide more robust agent-native fallback mechanisms for feature creation.