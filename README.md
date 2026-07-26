# 📝 DevPastes (Markdown Snippet Sharing)

A fast, lightweight full-stack web application designed for creating, previewing, and instantly sharing temporary Markdown code snippets with automated expiration.

---

## ✨ Features

- **Real-Time Markdown Preview:** Instant split-screen rendering powered by Ant Design and custom React components.
- **Automated Snippet Expiration:** In-memory snippet lifespan management built into the backend using Python `datetime` and `timedelta`.
- **Configurable Rate Limiting:** Protected API endpoints to prevent spam and resource exhaustion.
- **API Key Security Gate:** Secure route protection using standard HTTP headers.
- **Clean Architecture:** Modular folder structure isolating React components, CSS, and FastAPI endpoints.

---

## 🛠️ Tech Stack

### **Frontend**
- **Framework:** React + Vite (TypeScript)
- **UI Library:** Ant Design (AntD)
- **Styling:** Modular CSS & Flexbox
- **HTTP Client:** Axios

### **Backend**
- **Framework:** FastAPI (Python)
- **Web Server:** Uvicorn / `a2wsgi`
- **Environment Management:** `python-dotenv` / `pydantic-settings`
- **Security & Limits:** `slowapi` & FastAPI Security (`APIKeyHeader`)

---

## 📁 Repository Structure

```text
DEVPASTE/
├── .gitignore               
├── README.md
│
├── backend/          
│   ├── main.py              
│   └── requirements.txt
│
└── frontend/
    ├── .gitignore           
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    └── src/
        ├── api/             
        ├── assets/
        ├── components/
        ├── App.tsx
        ├── index.css
        └── main.tsx