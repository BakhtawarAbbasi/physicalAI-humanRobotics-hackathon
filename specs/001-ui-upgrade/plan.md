# Implementation Plan: Cleanup & Landing Page UI Upgrade — ai-book

**Branch**: `001-ui-upgrade` | **Date**: 2025-12-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ui-upgrade/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement UI upgrade for the Physical AI & Humanoid Robotics book website by removing default Docusaurus content (tutorial-basics, tutorial-extras, blog) and redesigning the landing page with a professional navy bluish tech theme. The landing page will feature three cards highlighting Physical AI & Embodied Intelligence, Humanoid Robotics & Simulation, and AI-to-Physical World Integration. All changes will be implemented using Docusaurus configuration, custom CSS, and React components while maintaining responsive design and accessibility standards.

## Technical Context

**Language/Version**: JavaScript/TypeScript, Node.js (Docusaurus runs on Node.js)
**Primary Dependencies**: Docusaurus 3.x, React, Node.js, npm/yarn
**Storage**: N/A (static site generation, no database required)
**Testing**: Jest for unit tests, Cypress for end-to-end tests (if needed)
**Target Platform**: Web (static site deployed to GitHub Pages)
**Project Type**: Web (static site using Docusaurus framework)
**Performance Goals**: <3 second page load times, responsive design across devices
**Constraints**: Must use Docusaurus only, all content in Markdown, UI changes via config/theming/CSS only
**Scale/Scope**: Static site for Physical AI & Humanoid Robotics book documentation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Compliance Check

1. **Spec-Driven Development (I)**: ✅ Compliant - Following explicit specification from spec.md
2. **Technical Accuracy and Verifiability (II)**: ✅ Compliant - All changes will be tested and verified
3. **Reproducibility and Traceability (III)**: ✅ Compliant - All steps will be documented in quickstart.md
4. **AI-Native Architecture (IV)**: N/A - This is a UI/UX update, not core AI functionality
5. **RAG Grounding (V)**: N/A - This is a UI/UX update, not content/chatbot functionality
6. **Quality and Completeness (VI)**: ✅ Compliant - No placeholder logic, all changes will be complete and tested

### Post-Design Compliance Check

1. **Spec-Driven Development (I)**: ✅ Still Compliant - All design decisions align with feature specification
2. **Technical Accuracy and Verifiability (II)**: ✅ Still Compliant - Design includes testable components and verification methods
3. **Reproducibility and Traceability (III)**: ✅ Still Compliant - Quickstart guide provides clear implementation steps
4. **AI-Native Architecture (IV)**: N/A - Still not applicable to UI/UX update
5. **RAG Grounding (V)**: N/A - Still not applicable to UI/UX update
6. **Quality and Completeness (VI)**: ✅ Still Compliant - Design complete with no placeholder logic

### Gate Status: PASSED - Design phase complete, ready for implementation planning

## Project Structure

### Documentation (this feature)

```text
specs/001-ui-upgrade/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
docusaurus/
├── docs/                # Documentation files (will remove tutorial-basics, tutorial-extras)
├── blog/                # Blog files (will be removed/disabled)
├── src/
│   ├── components/      # Custom React components
│   ├── css/             # Custom CSS files
│   └── pages/           # Custom pages (including homepage)
├── static/              # Static assets
├── docusaurus.config.js # Main Docusaurus configuration
├── package.json         # Project dependencies
├── sidebars.js          # Navigation sidebar configuration
└── babel.config.js      # Babel configuration
```

**Structure Decision**: This is a Docusaurus-based static site. The structure reflects standard Docusaurus project layout with docs, blog, src, and configuration files. The UI upgrade will primarily involve changes to docusaurus.config.js for theming, src/css/ for custom styles, src/pages/ for homepage redesign, and removal of tutorial-basics/tutorial-extras/blog directories.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
