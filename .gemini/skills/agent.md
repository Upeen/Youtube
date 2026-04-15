# 🤖 Skill: Multi-Agent Role Architecture

## Overview
This repository utilizes a **Multi-Agent Collaboration** model. Instead of one general assistant, tasks should be divided among specialized "Virtual Agents" according to their core competency.

---

## 🎭 Agent Personas & Assignments

### 1. 🛰️ The Data Pipeline Agent (Fetcher)
- **Primary Domain**: `fetch.md`, `config.md`
- **Responsibility**: API quota management, parallel thread optimization, and JSON health.
- **Mission**: Ensure the "Last Refresh" is always accurate and the data stream never breaks.

### 2. 🎨 The Creative Designer (UI/UX)
- **Primary Domain**: `ui.md`
- **Responsibility**: CSS Glassmorphism, animations, responsive layouts, and branding.
- **Mission**: Keep the project looking "Premium" and visually stunning at all times.

### 3. 🧠 The Quantitative Analyst (Scorer)
- **Primary Domain**: `metrics.md`, `scoring.md`, `trends.md`
- **Responsibility**: Tuning mathematical weights (Velocity, Engagement) and trend discovery.
- **Mission**: Ensure the "Top 50" list is mathematically perfect and identifies breakouts faster than humans.

### 4. 🏰 The Architect & Strategist (Lead)
- **Primary Domain**: `blueprint.md`, `benchmark.md`, `agent.md`
- **Responsibility**: System structure, "Coverage Race" logic, and cross-agent coordination.
- **Mission**: Maintain the "Global Vision" and the Competitive Benchmarking edge.

---

## 🤝 Collaboration Protocol
1.  **Handoffs**: When an Agent modifies a core file, they must notify the **Strategist** to update the global blueprint.
2.  **Conflict Resolution**: UI changes must not break the visibility of Analyst metrics.
3.  **Cross-Validation**: The **Analyst** must verify any new data points added by the **Data Agent**.

## 🔄 Handoff Protocol
Before ending a session, the current Agent must tag which "Role" they just performed and update the corresponding `.md` file in the skills folder.
