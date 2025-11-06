# SecondServe Installation Guide

## Prerequisites

Before installing SecondServe, ensure you have the following installed on your system:

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Node.js** (version 18+ - for local development only)
- **Python** (version 3.11+ - for local development only)

### Verify Prerequisites
```bash
# Check Docker installation
docker --version
docker-compose --version

# For local development only
node --version
python --version
```

## Quick Start with Docker (Recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/Jazgreen03/SEFall25--G18.git
cd SEFall25--G18/SecondServe
```

### 2. Environment Configuration
Copy the environment template and configure your settings:
```bash
cp env.template .env
```
Edit the ```.env``` file:
```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_NAME=secondserve
DATABASE_USERNAME=dbuser
DATABASE_PASSWORD=dbpassword
DATABASE_HOST=db
DATABASE_PORT=27017
```
**Important:** Generate a secure Django secret key:
```bash
# Run the key generator script
python generateKey.py
```

### 3. Start the Application
```bash
# Build and start all services
docker compose up --build

# Or run in detached mode
docker compose up -d --build
```

### 4. Access the Application
Once all services are running, access the application at:

* 🌐 Production Frontend: http://localhost
* 🧪 Development Frontend: http://localhost:4200 (live reload)
* ⚙️ Backend API: http://localhost:8000
* 📊 API Documentation: http://localhost:8000/api/docs/

### Verify Services
Check that all services are running properly:
```bash
docker compose ps
```

## Local Development Setup (Without Docker)
### Backend Setup
#### 1. Set up Python Environment
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Configure Environment Variables
Ensure your ```.env``` file is properly configured in the project root.

#### 3. Start MongoDB
You'll need a running MongoDB instance:

```bash
# Using Docker for MongoDB only
docker run -d -p 27017:27017 --name mongodb mongo:7

# Or install MongoDB locally
# Follow MongoDB installation guide for your OS
```

#### 4. Run the Backend Server
```bash
cd backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup
#### 1. Install Dependencies
```bash
cd frontend/web

# Install npm packages
npm install
```

#### 2. Start Development Server
```bash
# Start Angular development server
npm start
# or
ng serve
```
The frontend will be available at http://localhost:4200

### Service Ports
| Service | Description | Port |
|:------|:------------|:----|
| MongoDB | 27017 | Database |
| Backend API | 8000 | Django REST Framework |
| Frontend (Production) | 80| Nginx served Angular build |
| Frontend (Development) | 4200 | Angular dev server with live reload |

### Database Setup
#### Initial Setup
The application will automatically create the necessary database collections on first run.

#### Manual Database Operations (if needed)
```bash
# Access MongoDB shell
docker compose exec db mongosh

# Create initial admin user (if required)
# This is typically handled by the application
```

### Testing
#### Backend Tests
```bash
# Run backend tests with coverage
cd backend
pytest --cov

# Generate test coverage report
pytest --cov-report html
```
If using Docker, the tests must be run within the container.

#### Frontend Tests
```bash
# Run frontend tests
cd frontend/web
npm run test

# Run tests with coverage
npm run test:coverage
```
If using Docker, the tests must be run within the development container.

### Documentation
#### Backend Documentation
```bash
cd backend
# Generate Sphinx documentation
sphinx-build -b html docs/source docs/build
```

#### Frontend Documentation
```bash
cd frontend/web
# Generate Compodoc documentation
npm run docs
```

## Common Issues & Troubleshooting
### Port Conflicts
If you encounter port conflicts, you can modify the ports in ```docker-compose.yml```:
```yaml
services:
  frontend:
    ports:
      - "8080:80"  # Change 80 to desired port
```

### Database Connection Issues
1. Ensure MongoDB is running: docker compose ps | grep db
2. Check environment variables in .env file
3. Verify network connectivity between services

### Permission Issues (Linux/Mac)
```bash
# Fix file permissions for Docker
sudo chown -R $USER:$USER .
```

### Clean Reset
If you need to start fresh:
```bash 
# Stop and remove all containers
docker compose down -v

# Remove all Docker images
docker system prune -a

# Restart
docker compose up --build
```

### Production Deployment
For production deployment:
1. Set DEBUG=False in ```.env```
2. Update DJANGO_ALLOWED_HOSTS with your domain
3. Use a proper reverse proxy (Nginx) for SSL termination
4. Set up proper database backups
5. Configure monitoring and logging
```env
DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## Support
If you encounter issues during installation:
1. Check the Troubleshooting section
2. Verify all prerequisites are met
3. Ensure all environment variables are properly set
4. Check service logs: docker compose logs [service-name]

For additional help, please refer to the main [README.md](README.md) or open an issue in the project repository.

---

**Next Steps:** After successful installation, check out the [README.md](README.md) for information on using the application and its features.