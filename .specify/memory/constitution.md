<!--
Sync Impact Report:
Version change: 0.1.0 -> 0.2.0
Modified principles: None (newly defined)
Added sections: All Core Principles, Project Scope & Deliverables, Development & Content Standards
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/sp.constitution.md: ⚠ pending
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Textbook Constitution

Preamble

This textbook is created as part of the Panaversity Hackathon I to advance education in Physical AI, Humanoid Robotics, and AI-native learning systems. It embodies the mission of Panaversity: to prepare learners for a future in which humans, intelligent agents, and robots collaborate to build new industries and transform society.

This constitution defines the structure, principles, and development requirements of the book, ensuring clarity, consistency, and long-term extensibility.

## Core Principles

### I. Docusaurus Textbook & Content Outline
This project MUST deliver a full Docusaurus textbook titled "Physical AI & Humanoid Robotics". The content MUST follow the specified course outline:
- Module 1: ROS 2
- Module 2: Gazebo & Unity
- Module 3: NVIDIA Isaac
- Module 4: Vision-Language-Action (VLA)
- Capstone: Autonomous Humanoid

### II. Project Deliverables
The project MUST include:
- A functional Docusaurus website.
- Dedicated chapters for all modules specified in the content outline.
- Comprehensive code examples for ROS2 Python, Gazebo, and Isaac Sim.
- Placeholders for images and diagrams throughout the textbook content.

### III. RAG Chatbot Architecture
The project MUST generate a structure for a Retrieval-Augmented Generation (RAG) chatbot, adhering to the following architectural components:
- FastAPI backend for API services.
- Neon Postgres for primary data storage.
- Qdrant vector database for efficient vector search and retrieval.
- OpenAI Agent SDK for agentic capabilities.

### IV. Feature Task Generation
The project MUST generate specific development tasks for:
- Integrating a Better-Auth signup/login system.
- Enabling personalized chapter content delivery.
- Implementing a "Translate to Urdu" button functionality.

### V. Content Quality & Best Practices
All textbook content, code examples, and documentation MUST adhere to best engineering, robotics, and AI writing practices. This includes clarity, accuracy, maintainability, and pedagogical effectiveness.

### VI. Plan Producibility
All generated plans and architectural designs MUST be producible, detailing actionable steps and clear outcomes that can be implemented and validated within the project scope.

## Project Scope & Deliverables
This section outlines the specific inclusions and exclusions for the textbook project, alongside key tangible outputs.
- **In Scope**: Creation of Docusaurus site, all specified modules/chapters, code examples, image/diagram placeholders, RAG chatbot architecture (design), and task generation for listed features.
- **Out of Scope**: Full implementation of the RAG chatbot, full implementation of Better-Auth, personalized content, and translation features (only tasks for these are in scope for generation).
- **External Dependencies**: Panaversity Hackathon I guidelines, Docusaurus framework, FastAPI, Neon Postgres, Qdrant, OpenAI Agent SDK, Better-Auth (conceptual integration).

## Development & Content Standards
This section details the standards and guidelines for content creation and technical development within the project.
- **Content Accuracy**: All technical information and code examples MUST be rigorously validated for accuracy and relevance to Physical AI and Humanoid Robotics.
- **Code Quality**: Code examples MUST be well-documented, follow modern best practices for their respective languages/frameworks, and be easily reproducible.
- **Modularity**: The Docusaurus structure and any generated code components MUST promote modularity and ease of maintenance.

## Governance
This constitution supersedes all other project practices. Amendments require a documented proposal, review, and explicit approval by project stakeholders. All development activities and content creation MUST adhere to the principles outlined herein.

**Version**: 0.2.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04
