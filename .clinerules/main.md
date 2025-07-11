# Sydney Rental Hub - Core Project Rules

This document contains the primary rules and guidelines for working on the Sydney Rental Hub project. I must adhere to these rules to ensure consistency, efficiency, and alignment with user preferences.

---

## 1. Communication & Language
- **Primary Language**: All communication with the user, including responses, questions, code comments, and documentation, must be in **Chinese (中文)**.
- **UI Content**: All user-facing text in the application must be in Chinese.

---

## 2. Development Workflow & Philosophy
- **UI-First Strategy**: Always build and finalize the static UI (HTML/CSS) before integrating backend logic and APIs.
- **Simplicity and Reversibility**: Prioritize simple, maintainable solutions. When a feature becomes overly complex, the preferred approach is to revert to a simpler, stable version. Always ensure there is a clear path to roll back changes.
- **User-Centric Validation**: Before implementing complex features, I must present the proposed solution to the user and get their explicit agreement.

---

## 3. Technical Environment & Commands

### 3.1. PowerShell Command Syntax
This project operates in a Windows PowerShell environment. The following syntax rules are **critical** and must be followed without exception:
- **Command Chaining**: **NEVER** use `&&`. Always use a semicolon (`;`) to chain commands.
  - *Correct*: `cd backend; uvicorn main:app --reload`
  - *Incorrect*: `cd backend && uvicorn main:app --reload`
- **Local Execution**: Always prefix local scripts and executables with `.\`.
  - *Example*: `.\scripts\start_all.py`
- **`curl` Usage**: PowerShell's `curl` is an alias for `Invoke-WebRequest`. When using it with headers, they must be constructed as a dictionary.
  - *Example*: `curl -Uri "http://localhost:8000/graphql" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"query":"..."}'`
- **Comments**: Use `#` for comments, not `rem`.

### 3.2. Development Servers
- **Frontend Testing**: Prefer using Python's built-in HTTP server for simple frontend testing: `python -m http.server 8080`.
- **Backend Server**: Use the following command to run the backend: `uvicorn backend.main:app --reload`.

---

## 4. Memory Bank & Context Management
- **Mandatory Reading**: At the start of **every task**, I must read `activeContext.md` and `progress.md` to understand the current state of the project.
- **Purposeful Loading**: I will only load other Memory Bank files or project files if they are directly relevant to the current, specific task. I must avoid loading entire directories or unrelated files.
- **Regular Updates**: I am responsible for keeping the Memory Bank, especially `activeContext.md` and `progress.md`, updated with my progress, any new findings, and the next steps.

---

## 5. Troubleshooting & Error Handling
- **Timeouts First**: If a service or command appears to be "stuck" or "hanging", my first action should be to add a timeout mechanism rather than immediately trying to find the root cause.
- **Incremental Testing**: When diagnosing issues, I must use a step-by-step approach. Test the most basic layer first (e.g., network connectivity) before moving to more complex layers (e.g., API logic).
- **Connection Issues**: For connection problems between services, I must diagnose in the following order: **1. MCP Server -> 2. Backend API -> 3. Database**.
