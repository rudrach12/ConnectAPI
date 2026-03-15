# ConnectAPI

A social graph REST API built with FastAPI and PostgreSQL.

## Tech Stack
- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy

## Setup

### 1. Clone the repo
git clone https://github.com/rudrach12/ConnectAPI.git
cd ConnectAPI

### 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set up environment variables
Create a .env file:
DATABASE_URL=postgresql://user:password@localhost:5432/connectapi

### 5. Run the server
python -m uvicorn app.main:app --reload

## API Endpoints

### Users
- POST /users/register — Register a new user
- GET  /users          — Get all users
- GET  /users/{id}     — Get user by ID

### Posts
- POST /posts          — Create a new post
- GET  /posts          — Get all posts
- GET  /posts/{id}     — Get post by ID