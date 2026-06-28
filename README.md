# Benchmark System (Full-Stack)

> This project was developed during my internship at Hitec as part of a full-stack backend performance analysis and benchmarking system.

A full-stack performance benchmarking system built with **FastAPI (backend)** and **React (frontend)** to compare the behavior of different Python ASGI servers (**Uvicorn vs Gunicorn**) under synchronous and asynchronous workloads. The system collects performance metrics such as response time, CPU usage, memory consumption, and error rates, and visualizes results through a React UI and Streamlit dashboards.

---

## Internship Context

This project was developed during my internship at **Hitec**, where I worked on backend performance testing and full-stack system development. The goal was to evaluate and compare the performance characteristics of different server configurations under realistic workloads and present the results in a user-friendly interface.

---

## Architecture Overview

```text id="arch3"
React Frontend
│
├── Login / Register UI
├── Benchmark Dashboard
├── Chat / Results Views
│
FastAPI Backend
│
├── Uvicorn Benchmark API
├── Gunicorn Benchmark API
├── Authentication & Database Layer
├── CSV Logging & Analytics
│
Data Layer
├── MySQL / SQLAlchemy
├── Pandas Analysis
│
Visualization
├── Streamlit Dashboards
```

---

## Features

### Backend (FastAPI)

* Benchmarking async & sync workloads
* Uvicorn vs Gunicorn performance comparison
* CPU-intensive task simulation
* Memory and CPU monitoring (psutil)
* REST API for benchmark execution
* Data persistence with SQLAlchemy
* CSV logging for analytics
* Statistical aggregation (Pandas)
* Database management endpoints

---

### Frontend (React)

* User authentication (Login/Register)
* JWT token handling
* Protected routes
* Benchmark interaction UI
* API communication with backend
* Responsive interface
* State management with React Hooks
* Navigation using React Router

---

## Tech Stack

### Backend

* Python 3.11
* FastAPI
* Uvicorn
* Gunicorn
* SQLAlchemy
* Pandas
* Streamlit
* Psutil
* PyMySQL

### Frontend

* React
* JavaScript (ES6+)
* React Router DOM
* Axios / Fetch API
* CSS3

---

## Benchmark Categories

### Async Benchmark

* Non-blocking execution using `asyncio.to_thread`
* Simulates concurrent workload handling

### Sync Benchmark

* Blocking CPU-intensive execution
* Used for performance comparison

---

## API Endpoints

### Benchmark APIs

| Method | Endpoint                       | Description                |
| ------ | ------------------------------ | -------------------------- |
| GET    | `/get_async_uvicorn_function`  | Async benchmark (Uvicorn)  |
| GET    | `/get_sync_uvicorn_function`   | Sync benchmark (Uvicorn)   |
| GET    | `/get_async_gunicorn_function` | Async benchmark (Gunicorn) |
| GET    | `/get_sync_gunicorn_function`  | Sync benchmark (Gunicorn)  |

---

### Authentication (if included in frontend integration)

| Method | Endpoint    | Description       |
| ------ | ----------- | ----------------- |
| POST   | `/register` | Create user       |
| POST   | `/login`    | Authenticate user |

---

## Dashboards

* Benchmark Overview (response times)
* Hardware Metrics (CPU / Memory usage)
* Statistical Analysis (min / avg / max trends)

Run locally:

```bash id="dash1"
streamlit run benchmark_overview.py
streamlit run hardware_app.py
streamlit run stats_app.py
```

---

## Installation

### 1. Clone repository

```bash id="install1"
git clone https://github.com/yourusername/benchmark-system.git
cd benchmark-system
```

---

### 2. Backend Setup

```bash id="install2"
pip install -r requirements.txt
uvicorn main:app --reload
```

Or with Gunicorn:

```bash id="install3"
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

### 3. Frontend Setup

```bash id="install4"
cd frontend
npm install
npm start
```

---

## Key Learnings

This project demonstrates experience in:

* Full-stack application development
* Backend performance engineering
* Async vs sync system behavior
* Server benchmarking (Uvicorn vs Gunicorn)
* REST API design
* React frontend development
* Authentication and JWT handling
* Data analysis with Pandas
* System architecture design
* Real-world internship engineering workflow

---

## Future Improvements

* Docker Compose (frontend + backend + DB)
* Real-time WebSocket metrics
* Prometheus + Grafana monitoring
* Load testing with Locust
* PostgreSQL migration
* CI/CD pipeline integration
* Cloud deployment (AWS / Azure)
* Role-based authentication

---

## Security Notes

* Move all credentials to environment variables
* Secure API endpoints with authentication
* Disable debug mode in production
* Restrict database access in production environments

---

## Author

Developed during an internship at **Hitec** as a full-stack performance benchmarking system using FastAPI and React.
