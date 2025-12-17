---
description: "Task list for Cleanup & Landing Page UI Upgrade feature implementation"
---

# Tasks: Cleanup & Landing Page UI Upgrade — ai-book

**Input**: Design documents from `/specs/001-ui-upgrade/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Docusaurus project**: `docs/`, `blog/`, `src/`, `static/` at repository root
- **Configuration**: `docusaurus.config.js`, `sidebars.js` at repository root
- **CSS**: `src/css/custom.css`
- **Pages**: `src/pages/index.js`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Verify project structure and dependencies per plan.md
- [X] T002 [P] Install Docusaurus dependencies with npm install
- [X] T003 [P] Verify development server starts with npm run start

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Verify current site structure and identify default Docusaurus content locations
- [X] T005 [P] Create backup of current configuration files (docusaurus.config.js, sidebars.js)
- [X] T006 [P] Create backup of current homepage (src/pages/index.js if exists)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Clean Up Default Docusaurus Content (Priority: P1) 🎯 MVP

**Goal**: Remove default Docusaurus content (tutorial-basics, tutorial-extras, blog) so readers see only book-related content without confusion.

**Independent Test**: Reader visits the site and sees only book-related content without any default Docusaurus tutorial content in docs/tutorial-basics/, docs/tutorial-extras/, or blog sections.

### Implementation for User Story 1

- [X] T007 [US1] Delete docs/tutorial-basics/ directory and all its contents
- [X] T008 [US1] Delete docs/tutorial-extras/ directory and all its contents
- [X] T009 [US1] Delete blog/ directory to remove blog functionality completely
- [X] T010 [US1] Update docusaurus.config.js to remove blog plugin if present
- [X] T011 [US1] Update sidebars.js to remove references to deleted content
- [X] T012 [US1] Verify all internal links still work correctly after content removal
- [X] T013 [US1] Test site builds successfully after content cleanup

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Enhanced Landing Page with Robotics-Focused Cards (Priority: P2)

**Goal**: Create a modern, professional landing page with three specific feature cards about Physical AI, Humanoid Robotics, and AI-to-Physical World Integration.

**Independent Test**: Reader lands on the homepage and sees three clearly designed feature cards with the specified topics: Physical AI & Embodied Intelligence, Humanoid Robotics & Simulation, and AI-to-Physical World Integration.

### Implementation for User Story 2

- [X] T014 [P] [US2] Create new homepage component in src/pages/index.js with feature cards
- [X] T015 [P] [US2] Implement first feature card: Physical AI & Embodied Intelligence
- [X] T016 [P] [US2] Implement second feature card: Humanoid Robotics & Simulation
- [X] T017 [P] [US2] Implement third feature card: AI-to-Physical World Integration
- [X] T018 [US2] Ensure landing page design is responsive and readable on all devices
- [X] T019 [US2] Verify feature card titles match exactly: "Physical AI & Embodied Intelligence", "Humanoid Robotics & Simulation", "AI-to-Physical World Integration"

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Professional UI Theme Implementation (Priority: P3)

**Goal**: Implement a professional, modern, navy bluish tech-themed interface for consistent visual experience across the site.

**Independent Test**: Reader experiences the entire site with a unified navy bluish tech theme that feels professional and modern while maintaining readability and usability.

### Implementation for User Story 3

- [X] T020 [P] [US3] Define navy bluish color palette in CSS variables in src/css/custom.css
- [X] T021 [P] [US3] Implement primary theme colors: --ifm-color-primary: #1a365d
- [X] T022 [P] [US3] Implement secondary and accent colors for the navy bluish theme
- [X] T023 [US3] Apply theme consistently across all site components
- [X] T024 [US3] Ensure color contrast meets WCAG AA compliance (minimum 4.5:1)
- [X] T025 [US3] Test theme across different browsers and devices
- [X] T026 [US3] Update docusaurus.config.js to use new color scheme

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T027 [P] Update documentation to reflect new site structure in README.md
- [X] T028 Code cleanup and refactoring of CSS and component code
- [X] T029 [P] Run accessibility tests to ensure WCAG compliance
- [X] T030 Performance optimization to maintain <3 second load times
- [X] T031 [P] Cross-browser testing on Chrome, Firefox, Safari, Edge
- [X] T032 Run quickstart.md validation steps to ensure all works correctly
- [X] T033 Final site build and serve test to verify production build works

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (content cleanup) being complete
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Can work in parallel with US1/US2 but should be independently testable

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all feature cards for User Story 2 together:
Task: "Implement first feature card: Physical AI & Embodied Intelligence in src/pages/index.js"
Task: "Implement second feature card: Humanoid Robotics & Simulation in src/pages/index.js"
Task: "Implement third feature card: AI-to-Physical World Integration in src/pages/index.js"
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
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
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