# DermaFast - Full Stack Application

A full-stack application built with React + Vite, FastAPI, and Supabase.

## Project Structure

```
/frontend          # React + Vite frontend
/backend           # FastAPI backend
```

## Project Setup

Before running the application, you need to set up both the frontend and backend environments.

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

### 2. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(On Windows, use `.\venv\Scripts\activate`)*

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

## Running the Application

Once the setup is complete, you can run the application using one of the following methods.

### Manual Startup

You'll need two separate terminals to run the frontend and backend servers independently.

1.  **Start the backend server:**
    ```bash
    # In the /backend directory with venv activated
    python run.py
    ```
    The backend API will be available at http://localhost:8000.

2.  **Start the frontend server:**
    ```bash
    # In the /frontend directory
    npm run dev
    ```
    The frontend will be available at http://localhost:5173.

### Using Helper Scripts

Several Python scripts are provided in the root directory to simplify the process of stopping and starting the servers.

#### `restart_servers_simple.py` (Recommended)

This script stops any running server processes and restarts them in the background. It does not require any additional dependencies.

```bash
# From the project root directory
python3 restart_servers_simple.py
```

#### `restart_servers.py`

A more advanced script that provides more detailed output and remains running to monitor the server processes. You can stop both servers by pressing `Ctrl+C`. This script requires the `psutil` package.

```bash
# First, install the dependency
pip install psutil

# Run the script from the project root
python3 restart_servers.py
```

#### `restart.py`

An ultra-minimalist script for restarting the servers. It's quick but provides less feedback than the other scripts.

```bash
# From the project root directory
python3 restart.py
```

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
