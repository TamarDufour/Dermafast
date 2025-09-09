# DermaFast - Full Stack Application

A full-stack application built with React + Vite, FastAPI, and Supabase.

## Project Structure

```
/frontend          # React + Vite frontend
/backend           # FastAPI backend
```

## Setup Instructions

To run the application, you'll need two separate terminal windows: one for the backend and one for the frontend.

### 1. Environment Variables (Frontend)

The frontend uses Supabase for authentication. You'll need to provide your Supabase credentials in an environment file.

1.  Navigate to the `frontend` directory.
2.  Create a `.env` file inside the `frontend` directory.
3.  Add the following variables to `frontend/.env`, replacing the placeholder values with your actual Supabase credentials:

    ```env
    # Supabase Configuration
    VITE_SUPABASE_URL=your_supabase_project_url_here
    VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
    ```

You can get these values from your Supabase project dashboard at [https://supabase.com/dashboard](https://supabase.com/dashboard).

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the backend server:**
    ```bash
    python run.py
    ```

The backend API will be available at http://localhost:8000.
API documentation will be available at http://localhost:8000/docs.

### 3. Frontend Setup (Terminal 2)

```bash
# Go to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the frontend development server
npm run dev
```
The frontend will be available at http://localhost:5173.

## Features

- **Frontend**: React with Vite, Tailwind CSS, Supabase authentication
- **Backend**: FastAPI with health check and placeholder auth routes
- **Database**: Supabase for user management and authentication

## Next Steps

1.  Set up your Supabase project.
2.  Configure environment variables as described above.
3.  Run both frontend and backend.
4.  Implement actual authentication logic in the backend.
5.  Add more features as needed.
