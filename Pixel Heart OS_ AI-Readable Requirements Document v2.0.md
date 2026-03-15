# Pixel Heart OS: AI-Readable Requirements Document v2.0

## 1. System Overview
"Pixel Heart OS" is an AI-driven, emergent social universe system built around a central heroine character. It features a Git-style memory management system known as Beads, multi-agent simulation powered by LangGraph, and a pixel-art UI frontend utilizing Svelte 5 and Phaser 3. The system allows users to create a heroine from free-form descriptions, automatically generates a surrounding social network including NPCs and scenes, and simulates interactions with full state persistence and branching possibilities.

## 2. Technology Stack & Architecture

### 2.1 Frontend Architecture
The frontend is designed as a highly interactive, pixel-art web application that leverages modern web technologies for optimal performance and developer experience.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | Svelte 5 | Utilizes the new Runes system (`$state`, `$derived`, `$effect`) for universal reactivity, offering a tiny bundle size (~15kb) and direct DOM manipulation. |
| **Game Engine** | Phaser 3 (v3.90.0) | Renders the relationship nebula, pixel-art scenes, and the Beads timeline without virtual DOM conflicts. |
| **Integration** | `PhaserGame.svelte` | Acts as a bridge component. Communication between Svelte and Phaser is handled via an `EventBus`, emitting events like `current-scene-ready`. |
| **UI Styling** | Tailwind CSS | Combined with custom pixel-art CSS patterns to create blocky borders and retro fonts. |
| **State Management** | Svelte 5 Runes | Replaces traditional stores for global state, using exported `$state` objects or ES6 classes wrapped in `$state` for cross-component reactivity. |

### 2.2 Backend Architecture
The backend handles AI orchestration, memory management, and API endpoints, ensuring robust and scalable performance.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **API Framework** | FastAPI (Python) | Utilizes asynchronous endpoints (`async def`) for high concurrency and fast response times. |
| **Multi-Agent Engine** | LangGraph | Orchestrates complex, stateful multi-agent workflows, managing the parallel processing of NPCs and information flow. |
| **Memory System** | Custom Beads System | A Git-like version control system for narrative state, structured as a Directed Acyclic Graph (DAG). |
| **File Storage** | File System | Stores character souls, identities, and scene configurations as Markdown (`.md`) and TOML (`.toml`) files. |
| **Relational DB** | SQLite | Indexes Beads relationships and metadata for quick querying. |
| **Vector DB** | ChromaDB / Qdrant | Enables semantic retrieval of past conversations and context for AI agents. |

## 3. Core Workflows

### 3.1 Heroine Creation (Input Layer)
Users can input data via three distinct modes: Free Description, Questionnaire, or Reality Import such as chat logs. An LLM parses this input to extract the "soul structure," identifying core traumas, defense mechanisms, ideal types, and scene preferences. The output generates `soul.md`, `identity.md`, and `voice.toml` files that define the heroine's core characteristics.

### 3.2 Universe Emergence (Generation Layer)
Based on the heroine's extracted soul structure, the system automatically generates a surrounding universe. This includes a Protector NPC reflecting trauma defense mechanisms, a Competitor NPC embodying ideal type conflicts, and a Shadow NPC representing repressed traits. Additionally, environments matching the heroine's preferences, such as a rainy window or a late-night store, are generated as scenes.

### 3.3 Simulation & Memory (Execution Layer)
The execution layer operates on a turn-based system where player actions trigger LangGraph agents to process information and update states. Every significant interaction is committed as a new Bead, forming a continuous timeline. Players have the ability to branch the timeline to explore alternative dialogue choices without losing the main progression, offering a deep, exploratory narrative experience.

### 3.4 AI Collaborative Editing
Users can actively refine the generated universe. If an NPC feels too stereotypical or lacks motivation, the user can flag it for refinement. The system uses specific prompts to deepen the NPC's soul, such as giving a protector their own trauma. Changes are presented in a diff format, allowing the user to review and approve the AI's edits before they are merged into the main timeline.

## 4. UI/UX Requirements

### 4.1 Visual Style
The aesthetic is defined by modern pixel art, featuring crisp edges, limited color palettes like retro neon or pastel, and blocky UI components. Animations rely on Svelte 5's built-in transitions, such as `{#key}` blocks, to ensure smooth UI state changes without the need for heavy external animation libraries.

### 4.2 Key Interfaces
The application features several critical interfaces to support the core workflows. The Creation Mirror serves as a terminal-like input interface for describing the heroine. The Beads Timeline is a visual Git tree rendered in Phaser, displaying nodes colored by emotion, with branches and the current HEAD clearly marked. The Relationship Nebula provides a dynamic, real-time visualization of character connections and emotional states. Finally, the Diff Viewer offers a side-by-side or inline comparison tool for reviewing AI edits to character files.

## 5. Technical Advantages of the Stack
The combination of Svelte 5 and Phaser provides significant technical advantages. Svelte's compiled nature and Runes system result in a minimal bundle size and direct DOM manipulation, which avoids virtual DOM conflicts with Phaser's canvas rendering. LangGraph offers robust state persistence and cyclical graph execution, which is superior to linear chains for managing complex NPC interactions. The custom Beads system provides unprecedented narrative control, allowing players to analyze relationship breakdowns and explore parallel universes seamlessly.

## References
[1] Svelte 5 Runes Documentation: https://svelte.dev/blog/runes
[2] Phaser 3.90.0 Release Notes: https://phaser.io/news/2025/05/phaser-v390-released
[3] LangGraph Multi-Agent Architecture: https://www.langchain.com/langgraph
[4] FastAPI Async Concurrency: https://fastapi.tiangolo.com/async/
