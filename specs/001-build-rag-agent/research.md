# Research: Build RAG Agent with OpenAI SDK

## Decision: OpenAI Agent SDK Integration
**Rationale**: Using the OpenAI Agent SDK provides the most straightforward way to create an AI agent with tool integration capabilities.
**Alternative Considered**: Direct OpenAI API usage without Agent SDK
**Choice**: OpenAI Agent SDK offers better tool integration and orchestration capabilities

## Decision: Single File Architecture
**Rationale**: Following the user's requirement for a single `agent.py` file in the backend folder for simplicity and modularity.
**Alternative Considered**: Multi-file structure with separate modules
**Choice**: Single file approach as specified in requirements

## Decision: Qdrant Integration Method
**Rationale**: Reusing existing Qdrant search logic from spec-2 ensures consistency and leverages proven implementation.
**Alternative Considered**: Direct Qdrant client integration
**Choice**: Call existing retrieval pipeline as specified in requirements

## Decision: Content Grounding Strategy
**Rationale**: Ensuring agent responds using only retrieved content prevents hallucination and maintains strict grounding in source material.
**Alternative Considered**: Allowing some general knowledge in responses
**Choice**: Strict grounding approach as required for RAG systems