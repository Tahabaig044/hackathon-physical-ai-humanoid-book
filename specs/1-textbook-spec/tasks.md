---

description: "Task list for Physical AI & Humanoid Robotics Textbook Project"
---

# Tasks: Physical AI & Humanoid Robotics Textbook Project

**Input**: Design documents from `/specs/1-textbook-spec/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus structure.

- [ ] T001 Create Docusaurus scaffold & config (docusaurus.config.js, package.json, README.md)
- [ ] T002 Generate all chapter markdown files (/docs/intro.md, /docs/module-*/ *.md)
- [ ] T003 Generate sidebar.js with category structure (sidebar.js)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for the RAG chatbot.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] Create FastAPI project skeleton (backend/app/main.py, backend/requirements.txt)
- [ ] T005 [P] Qdrant vector store integration (backend/app/qdrant_client.py)
- [ ] T006 [P] Neon DB schema for doc metadata & user profiles (backend/app/neon_schema.sql or backend/app/db_client.py)
- [ ] T007 Implement embeddings pipeline (backend/app/embeddings.py)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Ensure all Docusaurus textbook content is structured and accessible.

**Independent Test**: A user can navigate the Docusaurus site, open any chapter, and view its content, including code snippets and diagram placeholders.

### Implementation for User Story 1

- [ ] T008 [US1] Verify Docusaurus displays all module chapters and content correctly (Entire Docusaurus site)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Interact with RAG Chatbot (Priority: P2)

**Goal**: Enable interactive AI chatbot functionality through a widget and text highlighting.

**Independent Test**: A user can open the chat widget, type a question, and receive a relevant answer from the AI, or highlight text, trigger the "Ask AI" function, and get a contextual response.

### Implementation for User Story 2

- [ ] T009 [P] [US2] Add React components for ChatWidget and HighlightAskAI (/src/components/ChatWidget.jsx, /src/components/HighlightAskAI.jsx)
- [ ] T010 [US2] Frontend highlight flow + server endpoint (Docusaurus frontend, backend/app/main.py POST /ask endpoint)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 5 - Manage User Profile (Priority: P2)

**Goal**: Enable secure user signup, login, and profile management.

**Independent Test**: A user can successfully register, log in, update their profile with skills and hardware, and verify that changes are saved.

### Implementation for User Story 5

- [ ] T011 [US5] Signup & Signin using Better-Auth (Docusaurus frontend, backend/app/auth_routes.py, Neon Postgres)

**Checkpoint**: At this point, User Stories 1, 2 AND 5 should all work independently

---

## Phase 6: User Story 3 - Personalized Learning Experience (Priority: P3)

**Goal**: Provide content adaptation based on user skill level and hardware preferences.

**Independent Test**: A registered user can set their skill level and hardware profile, and observe that relevant sections of the textbook content (e.g., explanations, code examples) adjust accordingly.

### Implementation for User Story 3

- [ ] T012 [US3] Implement PersonalizeButton React component (/src/components/PersonalizeButton.jsx)
- [ ] T013 [US3] Personalize content by profile & level (Docusaurus frontend logic, dynamic markdown rendering)

**Checkpoint**: At this point, User Stories 1, 2, 5 AND 3 should all work independently

---

## Phase 7: User Story 4 - Access Textbook in Urdu (Priority: P4)

**Goal**: Enable one-click translation of textbook content into Urdu.

**Independent Test**: A user can click a "Translate to Urdu" button, and the current chapter's content dynamically changes to Urdu.

### Implementation for User Story 4

- [ ] T014 [US4] Implement TranslateUrduButton React component (/src/components/TranslateUrduButton.jsx)
- [ ] T015 [US4] Add Translate to Urdu button functionality (Docusaurus frontend logic, translation API integration)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, deployment, and submission preparation.

- [ ] T016 [P] GitHub Actions for build & deploy to GitHub Pages or Vercel (.github/workflows/deploy.yml)
- [ ] T017 [P] Create demo instructions and README for judges (README.md, demo_script.txt)
- [ ] T018 Unit/E2E smoke tests (tests/)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4, and P2 stories ordered by criticality)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - Critical for US3.
- **User Story 3 (P3)**: Can start after Phase 5 (US5) - Depends on user profile data.
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No direct dependencies on other stories apart from core content.

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch frontend component development and backend endpoint definition together:
Task: "Add React components for ChatWidget and HighlightAskAI"
Task: "Frontend highlight flow + server endpoint"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 5 → Test independently → Deploy/Demo
5. Add User Story 3 → Test independently → Deploy/Demo
6. Add User Story 4 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2 & 5
   - Developer C: User Story 3 & 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

# End of tasks.md
