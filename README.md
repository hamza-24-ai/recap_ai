<div align="center">

<img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=32&pause=1000&color=6366F1&center=true&vCenter=true&width=600&lines=Recap+AI;Multi-Agent+Meeting+Tracker;Cross-Session+Memory;Powered+by+LangGraph" alt="Typing SVG" />

### 🧠 A multi-agent system that turns raw meeting transcripts into structured, trackable action items

<img src="https://capsule-render.vercel.app/api?type=waving&color=6366F1&height=150&section=header" width="100%"/>

</div>

---

## 📌 About

Most transcription tools (Otter.ai, Fireflies) stop at giving you a transcript.

**Recap AI's** core idea is **cross-session memory** — it remembers action items from past meetings and automatically checks whether they were completed when a new, related transcript is uploaded.

> ⚠️ **This is a prototype**, built to explore multi-agent orchestration, real-time communication, and cross-session state persistence — not a polished production product (yet).

---

## 🔗 Pipeline Overview

```mermaid
graph LR
    A[📄 Raw Transcript] --> B[📝 Transcript Cleaner]
    B --> C[📋 Decision Extractor]
    B --> D[✅ Action Item Extractor]
    C --> E[💾 Memory / Tracker Agent]
    D --> E
    E --> F[🔍 Follow-up Checker]
    F --> G[📊 Dashboard]

    style A fill:#1e1e2e,stroke:#6366F1,color:#fff
    style B fill:#1e1e2e,stroke:#6366F1,color:#fff
    style C fill:#1e1e2e,stroke:#6366F1,color:#fff
    style D fill:#1e1e2e,stroke:#6366F1,color:#fff
    style E fill:#1e1e2e,stroke:#6366F1,color:#fff
    style F fill:#1e1e2e,stroke:#6366F1,color:#fff
    style G fill:#1e1e2e,stroke:#6366F1,color:#fff
```

## 🤖 The Five Agents

| Agent | Role |
|---|---|
| 📝 **Transcript Cleaner** | Normalizes the raw transcript and identifies speakers |
| 📋 **Decision Extractor** | Pulls out key decisions made during the meeting |
| ✅ **Action Item Extractor** | Identifies who was assigned what, and any deadlines |
| 💾 **Memory / Tracker Agent** | Saves new action items as pending |
| 🔍 **Follow-up Checker** | Compares a new transcript against previously pending items and updates status to `done`, `still pending`, or `overdue` |

Splitting the work across focused agents (instead of one big LLM call) makes the output more reliable, and each part is independently testable and improvable.

---

## ⚡ Real-Time Agent Progress

Instead of a plain loading spinner, the backend streams **live updates over WebSocket** — so as each agent starts and finishes its work, the frontend shows exactly what's happening in real time.

```
📝 Transcript Cleaner   ████████████████████ done
📋 Decision Extractor   ████████████████████ done
✅ Action Item Extractor ███████████░░░░░░░░ running...
💾 Memory/Tracker Agent  ░░░░░░░░░░░░░░░░░░░░ waiting
🔍 Follow-up Checker     ░░░░░░░░░░░░░░░░░░░░ waiting
```

---

## 🛠️ Tech Stack

<div align="center">

### Frontend
![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![REST API](https://img.shields.io/badge/REST_API-025E8C?style=for-the-badge&logo=fastapi&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=for-the-badge&logo=socketdotio&logoColor=white)

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![JWT](https://img.shields.io/badge/JWT_Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

### AI Stack
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI%2FGemini-412991?style=for-the-badge&logo=openai&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

### Storage
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)

</div>

---

## 🧩 Why Multiple Agents Instead of One LLM Call

A single prompt asked to "analyze and track everything" tends to produce shallow, unstructured output.

Splitting responsibility across narrow, well-defined agents produces:
- ✅ More reliable output
- 🧪 Independently testable components
- 🔧 Independently improvable pipeline stages
- ➕ Easy extension (new agents can be added without touching the rest)

---

## 🚀 Status

This is still a **prototype** — built to explore multi-agent orchestration, real-time communication over WebSocket, and state persistence across sessions, rather than just another single-prompt demo.

---

<div align="center">

### 💬 Feedback & discussion welcome

If you're working on similar problems — multi-agent pipelines, cross-session memory, or real-time agent streaming — feel free to open an issue or start a discussion.

<img src="https://capsule-render.vercel.app/api?type=waving&color=6366F1&height=100&section=footer" width="100%"/>

</div>
