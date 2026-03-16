# 🩻 Async Radiology Pipeline: Multimodal Edge AI

A highly scalable, asynchronous Machine Learning architecture designed to process heavy medical images (X-rays, endoscopy scans) without blocking the main web server. This microservice leverages a Redis message broker and Celery background workers to run multimodal Vision-Language Models (VLMs) at the edge, persisting explainable diagnoses to a secure SQL database.

## ⚙️ The Asynchronous Architecture

1. **The Web Layer (FastAPI):** Instantly ingests high-resolution medical images and returns a tracking `task_id` to the client, ensuring the API never freezes during model inference.
2. **The Message Broker (Redis via Docker):** Acts as an in-memory queue, reliably holding pending image processing tasks.
3. **The Distributed Kitchen (Celery):** Background worker nodes that pull tasks from Redis and execute the heavy ML workloads independently.
4. **The Multimodal Brain (Moondream/LLaVA):** Edge-optimized Vision-Language Models that translate image pixels into clinical text.
5. **The Persistent Vault (SQLite & SQLAlchemy):** Permanently records the patient ID, image reference, exact timestamp, and the AI's Explainable AI (XAI) output for medical auditing.

## 🛠️ Tech Stack
* **API Framework:** FastAPI, Uvicorn
* **Task Queue & Broker:** Celery, Redis (Dockerized)
* **Relational Database (ORM):** SQLite, SQLAlchemy
* **Local Multimodal AI:** Ollama (Moondream/LLaVA)
