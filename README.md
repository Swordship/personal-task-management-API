# Personal Task Manager API

A RESTful API for personal task management built with FastAPI and MongoDB. Features complete CRUD operations, advanced filtering, search functionality, and task completion tracking.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Features

- **Complete CRUD Operations**: Create, read, update, and delete tasks
- **Advanced Filtering**: Filter tasks by completion status
- **Search Functionality**: Search through task titles and descriptions
- **Sorting**: Sort tasks by different fields (title, completion status, creation date)
- **Task Completion Toggle**: Mark tasks as complete or incomplete
- **Statistics**: Get real-time statistics about task completion
- **MongoDB Integration**: Persistent data storage with MongoDB Atlas
- **Async Operations**: Fast, non-blocking database operations
- **Data Validation**: Robust input validation with Pydantic
- **Auto Documentation**: Interactive API documentation with Swagger UI
- **Docker Support**: Containerized deployment ready

## API Demo

### Interactive API Documentation
![API Documentation](https://via.placeholder.com/800x400/009688/white?text=FastAPI+Swagger+UI+Documentation)

*Access interactive API documentation at `/docs` endpoint*

### Task Management Interface
![Task Operations](https://via.placeholder.com/800x300/4EA94B/white?text=CRUD+Operations+-+Create+Read+Update+Delete)

*Complete task management with all CRUD operations*

### Real-time Statistics
![Statistics Dashboard](https://via.placeholder.com/600x300/2496ED/white?text=Task+Statistics+%26+Analytics)

*Get real-time completion rates and productivity metrics*

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for flexible data storage
- **Motor**: Async MongoDB driver for Python
- **Beanie**: Async MongoDB ODM (Object Document Mapper)
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: Lightning-fast ASGI server

## Project Structure

```
Task-Manager-API/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── database.py          # MongoDB connection configuration
│   └── models/
│       ├── __init__.py
│       └── task.py          # Task data model
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── .dockerignore           # Docker ignore file
├── .env                    # Environment variables
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- MongoDB Atlas account (or local MongoDB installation)
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Swordship/personal-task-management-API
   cd personal-task-management-API
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=task_manager
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Setup

![Docker Deployment](https://via.placeholder.com/600x200/2496ED/white?text=Docker+Containerized+Deployment)

1. **Build the Docker image**
   ```bash
   docker build -t my-task-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 my-task-api
   ```

## API Endpoints

### Health Check
- `GET /` - API health check
- `GET /about` - Project information

### Task Management
- `GET /tasks` - Get all tasks with optional filtering, searching, and sorting
- `GET /tasks/{task_id}` - Get a specific task
- `POST /add_task` - Create a new task
- `PUT /update_task/{task_id}` - Update an existing task
- `DELETE /remove_task/{task_id}` - Delete a task

### Task Status Management
- `PATCH /task/{task_id}/completed/` - Mark task as completed
- `PATCH /task/{task_id}/incompleted/` - Mark task as incomplete

### Statistics
- `GET /task/stats` - Get task completion statistics

## Query Parameters

### GET /tasks

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `completed` | boolean | Filter by completion status | `?completed=true` |
| `search` | string | Search in title and description | `?search=homework` |
| `sort` | string | Sort by field (task, completed, created_at, updated_at) | `?sort=created_at` |
| `order` | string | Sort order (asc, desc) | `?order=desc` |

**Example Queries:**
```
GET /tasks?completed=false&search=work&sort=created_at&order=desc
```

## Request/Response Examples

### Create a Task
```bash
POST /add_task
Content-Type: application/json

{
    "task": "Complete FastAPI tutorial",
    "description": "Learn FastAPI by building a task manager"
}
```

**Response:**
```json
{
    "_id": "60f7b3b3b3b3b3b3b3b3b3b3",
    "task": "Complete FastAPI tutorial",
    "description": "Learn FastAPI by building a task manager",
    "completed": false,
    "created_at": "2024-01-15T10:30:00.123Z",
    "updated_at": "2024-01-15T10:30:00.123Z"
}
```

### Get Task Statistics
```bash
GET /task/stats
```

**Response:**
```json
{
    "total_tasks": 10,
    "completed_tasks": 6,
    "incomplete_tasks": 4,
    "completion_percentage": 60.0,
    "summary": "You completed 6 out of 10 tasks!"
}
```

## MongoDB Integration

![MongoDB Atlas](https://via.placeholder.com/700x250/4EA94B/white?text=MongoDB+Atlas+Cloud+Database)

*Cloud-hosted MongoDB database with automatic scaling and backup*

### Data Models

#### Task Model
```python
{
    "_id": "MongoDB ObjectId",
    "task": "string (required, max 200 characters)",
    "description": "string (optional, max 1000 characters)",
    "completed": "boolean (default: false)",
    "created_at": "datetime (auto-generated)",
    "updated_at": "datetime (auto-updated)"
}
```

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
```

### Linting
```bash
flake8 app/
```

## Deployment

![Deployment Options](https://via.placeholder.com/800x200/009688/white?text=Cloud+Deployment+Options+-+Railway+Render+Heroku+AWS)

### Cloud Platforms
The application can be deployed on various cloud platforms:

- **Railway**: Automatic deployment from GitHub
- **Render**: Docker and Git-based deployment
- **Heroku**: Container deployment
- **DigitalOcean App Platform**: Docker deployment
- **AWS/GCP**: Container services

### Environment Variables
Set these environment variables in your deployment platform:
- `MONGODB_URL`: MongoDB connection string
- `DATABASE_NAME`: Database name (default: task_manager)

## Screenshots

### API Testing
![API Testing](https://via.placeholder.com/800x500/f8f9fa/333333?text=API+Testing+with+Postman+or+Thunder+Client)

*Testing API endpoints with various HTTP clients*

### MongoDB Compass
![MongoDB Compass](https://via.placeholder.com/800x500/4EA94B/white?text=MongoDB+Compass+Database+Management)

*Managing tasks data with MongoDB Compass GUI*

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Contact

**Developer**: Monish
**Email**: monishravi508@gmail.com  
**GitHub**: [@Swordship](https://github.com/Swordship)  
**Project Link**: [personal-task-management-API](https://github.com/Swordship/personal-task-management-API)

## Acknowledgments

- FastAPI documentation and community
- MongoDB documentation
- Beanie ODM documentation
- Python async programming resources