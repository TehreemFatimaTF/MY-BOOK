# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites

- Node.js 18+ for Docusaurus frontend
- Python 3.11+ for FastAPI backend
- Access to Neon Postgres database
- Access to Qdrant vector database
- OpenAI API key (or alternative LLM provider)
- Git for version control

## Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up backend environment:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend environment:**
   ```bash
   cd frontend
   npm install
   ```

4. **Configure environment variables:**
   Create `.env` files in both backend and frontend directories based on the `.env.example` files:

   Backend `.env`:
   ```
   DATABASE_URL=your_neon_postgres_connection_string
   QDRANT_URL=your_qdrant_connection_string
   QDRANT_API_KEY=your_qdrant_api_key
   OPENAI_API_KEY=your_openai_api_key
   BETTER_AUTH_SECRET=your_auth_secret
   BETTER_AUTH_URL=http://localhost:3000
   ```

   Frontend `.env`:
   ```
   BACKEND_API_URL=http://localhost:8000
   ```

## Running the Application

### Backend (FastAPI)

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Run the backend server:**
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

4. **The backend will be available at:** `http://localhost:8000`

### Frontend (Docusaurus)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **The frontend will be available at:** `http://localhost:3000`

## Initial Setup Tasks

1. **Populate the textbook content:**
   - Add your textbook chapters to the `frontend/docs/` directory following the structure defined in the plan
   - Update `frontend/sidebars.js` to include your new content in the navigation

2. **Index content for RAG:**
   - Run the content indexing script to populate Qdrant with textbook content:
   ```bash
   cd backend
   source venv/bin/activate
   python -m src.scripts.index_content
   ```

3. **Set up authentication:**
   - Better-Auth should work out of the box with the environment variables
   - Test authentication by visiting `/api/auth` endpoints

## API Endpoints

### Backend API (FastAPI)
- `GET /api/v1/health` - Health check
- `POST /api/v1/chat` - RAG chatbot endpoint
- `GET /api/v1/translate` - Translation endpoint
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login

### Frontend Routes
- `/` - Homepage
- `/docs/` - Textbook content
- `/why-choose-book` - Landing page
- `/ready-to-build-future` - Closing page

## Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### GitHub Pages Deployment
1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. The build output will be in the `frontend/build/` directory, ready for deployment to GitHub Pages.

### Backend Deployment
Deploy the FastAPI application to your preferred hosting platform (Heroku, Render, AWS, etc.) with the appropriate environment variables set.