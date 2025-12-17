<!--
Sync Impact Report:
- Version change: N/A -> 1.0.0 (initial version)
- Modified principles: N/A (new constitution)
- Added sections: Core Principles (6), Constraints, Development Workflow, Governance
- Removed sections: N/A
- Templates requiring updates: N/A
- Follow-up TODOs: None
-->
# AI/Spec-Driven Technical Book with Integrated RAG Chatbot Constitution

## Core Principles

### I. Spec-Driven Development
Spec-driven development (all work must follow explicit specifications). All technical work must be grounded in clear, written specifications before implementation begins. This ensures alignment between requirements and deliverables, reduces rework, and maintains project clarity.

### II. Technical Accuracy and Verifiability
All technical claims must be accurate and verifiable. Code examples must be complete, runnable, and clearly explained. Technical content must be implementation-ready and factually correct for the target audience of developers and AI engineers.

### III. Reproducibility and Traceability
All steps, configurations, and code must be reproducible and traceable. This includes maintaining clear documentation of environment variables, API keys, and configurations. All processes must be repeatable by others following the documentation.

### IV. AI-Native Architecture
AI-native architecture emphasizing agents, RAG, and tools-first design. Systems must leverage modern AI capabilities effectively while maintaining clean separation of concerns between ingestion, embedding, retrieval, and generation phases.

### V. RAG Grounding (NON-NEGOTIABLE)
Retrieval-Augmented Generation architecture is mandatory with strict grounding in book content only. No external hallucinated knowledge is allowed. The chatbot must respect selected-text-only query mode and provide answers strictly based on provided content.

### VI. Quality and Completeness
No placeholder logic or pseudo-code in final implementation sections. All code must be complete, tested, and production-ready. Documentation must be comprehensive and deployment processes clearly outlined.

## Constraints and Standards
Technology stack requirements and deployment policies as specified. Book must be deployed via GitHub Pages using Docusaurus. Backend stack includes OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, and Qdrant Cloud for vector search. All setup steps must be documented with clear environment variable descriptions.

## Development Workflow
Development follows Spec-Kit Plus methodology with clear separation between specification, planning, task generation, and implementation phases. All work must align with written specifications before implementation. Code reviews must verify compliance with constitutional principles. Testing and validation are mandatory for all deliverables.

## Governance

Constitution supersedes all other practices and guides all project decisions. All implementations must comply with these principles. Amendments require formal documentation and team approval. Quality gates include specification alignment, technical accuracy verification, and deployment validation.

**Version**: 1.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
