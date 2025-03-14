# Advanced User Management Portal

A comprehensive user management system with a MongoDB database, Python Flask backend API, and Vue.js frontend.

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Vue](https://img.shields.io/badge/vue-3.x-green.svg)

## Overview

The Advanced User Management Portal is a full-stack web application that provides functionality for managing users, including:

- User listing with search capabilities
- User creation, updating, and deletion
- Role management
- User preferences

The application consists of three main components:

1. **MongoDB Database**: Stores user data
2. **Flask Backend API**: RESTful API for data operations
3. **Vue.js Frontend**: Modern UI built with Vuetify component framework

## Architecture

### Database Initialization with parser.py

The project includes a data parser (`app/parser.py`) that initializes the MongoDB database with sample user data. Here's how it works:

- The parser reads user data from a JSON file (`udata.json`)
- It converts the JSON data into User objects with proper data types and structure
- When the backend container starts, it checks if the database is empty
- If no users exist, it automatically runs the parser to populate the database

The parser performs the following transformations:
- Maps user roles from boolean flags to a list of role strings
- Converts timestamps from ISO format to Unix timestamps
- Creates structured User objects with proper preferences

### Technology Stack

#### Backend
- **Python 3.12**: Modern Python version with performance improvements
- **Poetry**: Dependency management
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing support
- **PyMongo**: MongoDB client for Python
- **python-decouple**: Environment variable management

#### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vuetify 3**: Material Design component library
- **Vue Router 4**: Client-side routing
- **Axios**: HTTP client

#### Database
- **MongoDB**: NoSQL document database

#### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Web server and reverse proxy

## Running the Application

### Option 1: Using Docker (Recommended)

This is the easiest method as it handles all dependencies automatically.

#### Prerequisites
- Docker
- Docker Compose

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/thalissonvs/deeper-systems-test
   cd deeper-systems-test
   ```

2. Start the application:
   ```bash
   docker compose up --build
   ```

   This script will:
   - Build and start all containers
   - Initialize the database if needed
   - Display logs and status information

3. Access the application:
   - Frontend: http://localhost
   - API: http://localhost/api

4. To stop the application:
   ```bash
   docker compose down
   ```

### Option 2: Manual Setup

This option requires installing all dependencies on your local machine.

#### Prerequisites
- Python 3.12
- Poetry
- Node.js 16+ and npm
- MongoDB

#### Backend Setup

1. Install Python 3.12:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3.12 python3.12-venv python3.12-dev
   
   # macOS with Homebrew
   brew install python@3.12
   ```

2. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install backend dependencies:
   ```bash
   cd deeper-systems-test
   poetry install
   ```

4. Set up environment variables:
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit the .env file with your MongoDB connection details
   # For local development, you might use:
   # MONGO_USERNAME=admin
   # MONGO_PASSWORD=password
   # MONGO_HOST=localhost
   # MONGO_PORT=27017
   # MONGO_DB=app
   ```

5. Start MongoDB:
   ```bash
   # Using the system's MongoDB service
   sudo systemctl start mongodb
   
   # Or using Docker just for MongoDB
   docker run -d -p 27017:27017 --name mongodb \
     -e MONGO_INITDB_ROOT_USERNAME=admin \
     -e MONGO_INITDB_ROOT_PASSWORD=password \
     mongo:latest
   ```

6. Initialize the database:
   ```bash
   python -m app.parser
   ```

7. Start the Flask API server:
   ```bash
   python -m flask --app app.server.api run --host=0.0.0.0 --port=5000
   ```

#### Frontend Setup

1. Install Node.js and npm:
   ```bash
   # Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
   sudo apt install -y nodejs
   
   # macOS with Homebrew
   brew install node@16
   ```

2. Install frontend dependencies:
   ```bash
   cd app/client
   npm install
   ```

3. Start the development server:
   ```bash
   npm run serve
   ```

4. Build for production:
   ```bash
   npm run build
   ```

5. To serve the production build, you can use any web server:
   ```bash
   # Example using Python's http.server
   python -m http.server 8080
   ```

## API Endpoints

The backend provides the following RESTful endpoints:

- `GET /users`: Get all users
- `GET /users/:id`: Get a specific user
- `POST /users`: Create a new user
- `PUT /users/:id`: Update a user
- `DELETE /users/:id`: Delete a user

## Development

### Project Structure

```
.
├── app/
│   ├── client/           # Frontend Vue.js application
│   ├── docker/           # Docker configuration files
│   ├── models/           # Data models
│   ├── server/           # Backend API
│   ├── database.py       # Database connection
│   └── parser.py         # Data parser for initialization
├── docker-compose.yaml   # Docker Compose configuration
├── pyproject.toml        # Python dependencies
└── settings.py           # Application settings
```

