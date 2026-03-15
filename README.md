# AeroScribe ✈️
### AI-Powered Multi-Agent Decision Support for Air Traffic Control

AeroScribe is a real-time, high-stakes decision-support layer for Air Traffic Control (ATC) powered by **Microsoft Azure AI Foundry**. It solves the critical challenge of manual transcription and conflict detection in high-pressure aviation environments.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4.svg)
![Responsible AI](https://img.shields.io/badge/Responsible%20AI-Azure%20Content%20Safety-red.svg)
![MCP](https://img.shields.io/badge/MCP-Server-blueviolet.svg)

---

## 1. A Clear Problem & Real-World Use Case

### The Problem
Air Traffic Control relies on rapid-fire radio communication. Controllers must hear, interpret, and mentally cross-reference verbal instructions with a complex, moving field of aircraft and vehicles. **Information overload, phonetic ambiguity, and manual state tracking** are the primary drivers of runway incursions—one of the most dangerous risks in aviation.

### Our Solution
AeroScribe acts as a "second set of eyes and ears." It converts noisy radio speech into a structured digital twin of the airport, automatically detecting safety violations and providing strategic routing suggestions.

### Why It Matters
By automating the transcription and conflict-detection loop, AeroScribe reduces the cognitive load on controllers, ensures "Responsible AI" governance in safety-critical communications, and provides a discoverable API for the next generation of autonomous aviation agents.

---

## 2. Practical Use of Microsoft AI Technologies

AeroScribe is built on a sophisticated **4-agent orchestration pipeline** hosted on **Azure AI Foundry**:

1.  **Azure AI Content Safety (Responsible AI):** Every transcript is first screened for harmful content or misinformation that could compromise safety, ensuring the system fails-safe.
2.  **Azure OpenAI (GPT-4.1) - Transcription Agent:** Maps phonetically noisy STT (e.g., "maybe" vs "MAYDAY") into structured aviation JSON using contextual domain knowledge.
3.  **Azure OpenAI (GPT-4.1) - Safety Agent:** Audits every event against a real-time digital twin of the airport to flag runway incursions or unauthorized movements.
4.  **Azure OpenAI (GPT-4.1) - Strategic Planning Agent:** Provides on-demand, conflict-free routing suggestions based on current airport traffic.

### Technical Depth
The solution integrates **Model Context Protocol (MCP)**, allowing external agents (like VS Code Copilot or specialized aviation LLMs) to query the airport's live state, layout, and alerts via a standardized tool interface.

---

## 3. Working Solution & Prototype

AeroScribe includes a complete, end-to-end prototype:

-   **Real-Time Dashboard:** A high-performance, responsive UI (FastAPI/WebSockets) providing glassmorphic "Dark Mode" visuals of all active aircraft, current transcripts, and safety alerts.
-   **Aviation Digital Twin:** An in-memory state engine tracking runways (02L, 20R, etc.), taxiways, and platform locations.
-   **Simulation Engine:** A scripted radio simulator that demonstrates the full multi-agent pipeline and conflict detection logic without requiring a physical radio or microphone setup.
-   **Production-Ready Deployment:** Infrastructure-as-code scripts for one-click deployment to **Azure App Service**.

---

## 4. Documentation & Usage

### System Architecture
```text
aerscribe/
├── main.py                          # Entry point (Server, STT Listener, Simulator)
├── config.py                        # Azure Foundry & Content Safety settings
├── mcp_server.py                    # MCP Server (Model Context Protocol)
├── agent/
│   └── llm_processor.py             # Multi-Agent Orchestrator (4-agent pipeline)
├── state/
│   ├── aircraft_state.py            # Real-time state management
├── detection/
│   ├── conflict_detection.py        # Deterministic safety rules
├── dashboard/
│   └── templates/                   # Live operational UI
└── simulation/
    └── radio_simulator.py           # Pre-scripted test scenarios
```

### Setup Instructions
1.  **Clone & Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS
    pip install -r requirements.txt
    ```
2.  **Azure Configuration:**
    Set your `AZURE_FOUNDRY_API_KEY` and `AZURE_CONTENT_SAFETY_KEY` in your environment or `config.py`.

### How to Run
-   **Simulation Mode (Reviewer Recommended):** `python main.py --simulate`
-   **Live Microphone:** `python main.py`
-   **Automated Tests:** `pytest tests/`

---

## Media & Walkthroughs
*[Include space for Demo Video here]*
*[Include Dashboard Screenshot here]*

AeroScribe demonstrates how Microsoft Azure AI Foundry can bridge the gap between noisy human communication and safe, structured enterprise operations.
