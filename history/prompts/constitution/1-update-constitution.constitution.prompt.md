---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-16
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution,spec-driven-development,ai-book,rag-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution

Project: AI/Spec-Driven Technical Book with Integrated RAG Chatbot

Core principles:
- Spec-driven development (all work must follow explicit specifications)
- Technical accuracy and verifiability
- Clarity for a developer and AI-engineering audience
- Reproducibility (all steps, configs, and code must be traceable)
- AI-native architecture (agents, RAG, tools-first design)

Key standards:
- Book must be written and structured using Docusaurus
- Content must be generated using Claude Code guided by Spec-Kit Plus
- All technical claims must be accurate and implementation-ready
- Code examples must be complete, runnable, and clearly explained
- RAG chatbot answers must be grounded strictly in the book content

Chatbot & RAG standards:
- Retrieval-Augmented Generation architecture is mandatory
- Data source: book content only (no external hallucinated knowledge)
- Must support answering:
  - General questions about the book
  - Questions based solely on user-selected text
- Stack requirements:
  - OpenAI Agents/ChatKit SDKs
  - FastAPI backend
  - Neon Serverless Postgres for metadata/session storage
  - Qdrant Cloud (Free Tier) for vector search
- Clear separation of ingestion, embedding, retrieval, and generation phases

Constraints:
- Deployment:
  - Book must be deployed via GitHub Pages
- Documentation:
  - All setup steps must be documented
  - Environment variables, API keys, and configs clearly described
- Code quality:
  - No placeholder logic
  - No pseudo-code in final implementation sections
- AI behavior:
  - No speculative or unverifiable claims
  - No "vibe coding" or unexplained design decisions

Success criteria:
- Book builds successfully with Docusaurus and deploys on GitHub Pages
- Content is fully spec-aligned and technically correct
- Embedded RAG chatbot:
  - Runs without errors
  - Correctly retrieves and answers based on book content
  - Respects selected-text-only query mode
- Architecture and implementation pass technical review
- Project demonstrates clear AI-native, spec-driven design

## Response snapshot

The constitution file has been successfully updated with the project-specific principles and requirements. The new constitution includes six core principles:

1. Spec-Driven Development
2. Technical Accuracy and Verifiability
3. Reproducibility and Traceability
4. AI-Native Architecture
5. RAG Grounding (NON-NEGOTIABLE)
6. Quality and Completeness

It also includes sections for Constraints and Standards, Development Workflow, and Governance, all aligned with the project requirements for an AI/Spec-Driven Technical Book with Integrated RAG Chatbot.

## Outcome

- ✅ Impact: New project constitution created with 6 core principles and governance structure
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Plan development tasks using /sp.plan
- 🧠 Reflection: Constitution now provides clear governance framework for the AI/Spec-Driven Technical Book project

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Create feature specification using /sp.specify