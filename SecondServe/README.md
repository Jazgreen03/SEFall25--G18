# 🥫 SecondServe

<p align="center">
  <img src="https://img.shields.io/badge/Frontend-Angular-red?logo=angular&logoColor=white" />
  <img src="https://img.shields.io/badge/Backend-Django-0C4B33?logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-MongoDB-4EA94B?logo=mongodb&logoColor=white" />
  <img src="https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Language-Python-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Language-TypeScript-3178C6?logo=typescript&logoColor=white" />
  <img src="./frontend/web/documentation/images/coverage-badge-documentation.svg" />
  <img src="./backend/docs/source/_static/doc_coverage.svg" />
  <img src="./backend/docs/source/_static/test_coverage.svg" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
</p>

---

SecondServe is a full-stack platform built using **Angular**, **Django**, and **MongoDB**, designed as a student engineering project to manage food donations and deliveries efficiently between **organizations**, **drivers**, and **individual users**.  

The platform is containerized using **Docker Compose**, providing an easy-to-deploy development and production environment with automatic backend, frontend, and database orchestration.

---

## 📚 Table of Contents

1. [Overview](-🧩-Overvieww)
2. [Tech Stack](⚙️-tech-stack)
3. [Architecture](🏗️-architecture)
4. [Project Structure](🗂️-project-structure)
5. [Docker Setup](🐳-docker-setup)
6. [Environments](🌍-environments)
7. [Testing & Documentation](🔍-testing-&-documentation)
8. [Contributing](🤝-contributing)
9. [Future Enhancements](🧭-future-enhancements)
10. [License](🪪-license)

---

## 🧩 Overview

**SecondServe** connects donors, organizations, and delivery drivers to streamline the distribution of surplus food.  
It provides a real-time web interface for managing orders, deliveries, and donations through role-based access and dashboards.

**User Types:**
- 🧍 **User** – creates donation requests or posts food availability.  
- 🏢 **Organization** – manages incoming donations and monitors order history.  
- 🚚 **Driver** – accepts and completes delivery tasks assigned by organizations.

---

## ⚙️ Tech Stack

| Layer | Technology |
|:------|:------------|
| Frontend | Angular 20, TypeScript, TailwindCSS |
| Backend | Django 5 + Django REST Framework |
| Database | MongoDB (via `django-mongodb-backend`) |
| DevOps | Docker, Docker Compose, Nginx |
| Testing | Pytest (backend), Karma/Jasmine (frontend) |
| Documentation | Sphinx (backend), Compodoc (frontend) |

---

## 🏗️ Architecture

```text
+----------------------------------------------------+
|                      FRONTEND                      |
|            Angular (SSR / Dev / Nginx)             |
+------------------------|---------------------------+
                         |
                         | REST API
                         v
+----------------------------------------------------+
|                      BACKEND                       |
|                 Django + DRF                       |
|                 MongoDB Backend                    |
+------------------------|---------------------------+
                         |
                         | Mongoose Driver (ODM)
                         v
+----------------------------------------------------+
|                      DATABASE                      |
|                     MongoDB 7                      |
+----------------------------------------------------+
```
---
## 🗂️ Project Structure

```text
SecondServe/
│
├── backend/                  # Django backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── SecondServe/
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
│
├── frontend/
│   ├── web/                  # Angular project source
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── nginx.conf
│   └── proxy.conf.json
│
├── docker-compose.yaml
├── .env
└── README.md
```
---
## 🐳 Docker Setup

The system runs with 4 main services, all defined in compose.yaml:
| Service | Description | Port |
|:------|:------------|:----|
| db | MongoDB instance | 27017 |
| backend | Django API server | 8000 |
| frontend | Angular build served via Nginx (production)| 80 |
| frontend-dev | Angular live-reload dev server | 4200 |

### ✅ To start the stack
```bash
docker compose up --build
```

Once started
* 🌐 Frontend (Prod): http://localhost
* 🧪 Frontend (Dev): http://localhost:4200
* ⚙️ Backend API: http://localhost:8000
* 📦 MongoDB: mongodb://localhost:27017
---
## 🌍 Environments
All key environment variables are stored in .env:
```env
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost
DATABASE_NAME=dockerdjango
DATABASE_USERNAME=dbuser
DATABASE_PASSWORD=dbpassword
DATABASE_HOST=db
DATABASE_PORT=27017
```

The Django secret key can be generated using the ```generateKey.py``` script found in the project's root directory.
---
## Usage
### Running the Backend Locally
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

### Running the Angular Frontend Locally without Docker
```bash
cd frontend/web
npm install
npm start
```

### Building the Angular Documentation
```bash
npm run docs
```
---
## 🔍 Testing & Documentation
### Frontend
```bash 
npm run test:coverage
npm run docs
```
### Backend
While connected to the database through Docker container:
```bash 
pytest --cov
sphinx-build -b html docs/source docs/build
```
### Generated Badges:
* Angular Documentation Coverage
* Backend Documentation Coverage
* Backend Test Coverage
---
## 🤝 Contributing
Contributions are welcome!
To contribute:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/new-feature)
3. Commit your changes (git commit -m "Add new feature")
4. Push to your branch (git push origin feature/new-feature)
5. Open a Pull Request
---

## 🧭 Future Enhancements
* Map integration for deliveries
* Nutrition tracking and balancing for orders
* Special dietary instructions for deliveries
* Handling of donations to help support drivers
---
## 🪪 License

This project is licensed under the MIT License.

Copyright 2025 SecondServe

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Project Structure:
```
SecondServe/
├─ docker-compose.yml      # Docker configurations for running the project
├─ env.template
├─ .env                    # Local environment Variables
├─ README.md
├─ backend/                # The Django Project (handles Backend and Database functions)
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ manage.py
│  ├─ SecondServe/
│  |  ├─ __init__.py
|  |  ├─ apps.py           # Configurations to make sure ID's match with MongoDB defaults
│  |  ├─ settings.py       # Django settings used for Project management
│  |  ├─ urls.py           # API Call Routing (Primarily to the different apps)
|  |  ├─ asgi.py
│  |  └─ wsgi.py
│  ├─ Inventory/           # The Inventory "app" containing all Inventory-related functionality
│  |  ├─ __init__.py
|  |  ├─ apps.py           # Configurations to make sure ID's match with MongoDB defaults
│  |  ├─ models.py         # Data structures for Inventory and Item
│  |  ├─ urls.py           # API Call Routing
|  |  └─ views.py          # API Call Management and Execution
│  ├─ Organization/        # The Organization "app" containing all Organization-related functionality
│  |  ├─ __init__.py
|  |  ├─ apps.py           # Configurations to make sure ID's match with MongoDB defaults
│  |  ├─ models.py         # Data structures for Organization
│  |  ├─ urls.py           # API Call Routing
|  |  └─ views.py          # API Call Management and Execution
│  ├─ User/                # The User "app" containing all User-related functionality
│  |  ├─ __init__.py
|  |  ├─ apps.py           # Configurations to make sure ID's match with MongoDB defaults
│  |  ├─ models.py         # Data structures for User
│  |  ├─ urls.py           # API Call Routing
|  |  └─ views.py          # API Call Management and Execution
│  └─ testing/             # All the test cases for the backend
│     ├─ test_core.py
|     ├─ test_inventory_api.py
|     ├─ test_inventory_models.py
|     ├─ test_organization_api.py
|     ├─ test_user_api.py
│     └─ test_user_models.py
└─ frontend/               # The Angular Project (handles Frontend functions)
   ├─ Dockerfile
   ├─ nginx.conf           # NGINX Config -> Routes backend calls through/from frontend
   ├─ proxy.conf.json      # dev proxy to backend
   └─ web/                 # Angular workspace
```
