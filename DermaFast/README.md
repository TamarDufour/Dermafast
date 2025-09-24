# DermaFast - Full Stack Application

A full-stack application built with React + Vite, FastAPI, and Supabase.

## Project Structure

```
/frontend          # React + Vite frontend
/backend           # FastAPI backend
```

## Project Setup

Before running the application, you need to set up both the frontend and backend environments.

### 1. Environment Variables

#### Frontend

The frontend uses Supabase for authentication. You'll need to provide your Supabase credentials in an environment file.

1.  Navigate to the `frontend` directory.
2.  Create a `.env` file inside the `frontend` directory.
3.  Add the following variables to `frontend/.env`, replacing the placeholder values with your actual Supabase credentials:

    ```env
    # Supabase Configuration
    VITE_SUPABASE_URL=your_supabase_project_url_here
    VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
    ```

You can get these values from your Supabase project dashboard under **Project Settings > API**.

#### Backend

The backend requires separate credentials to communicate with Supabase.

1.  Navigate to the `backend` directory.
2.  Create a `.env` file inside the `backend` directory.
3.  Add the following variables to `backend/.env`:

    ```env
    # Supabase Configuration
    SUPABASE_URL=your_supabase_project_url_here
    SUPABASE_SERVICE_KEY=your_supabase_service_role_key_here
    ```

The `SUPABASE_URL` is the same as the one used in the frontend. The `SUPABASE_SERVICE_KEY` can also be found in your Supabase project's API settings. **Warning: Keep your service role key confidential and never expose it in client-side code.**

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

### 4. Database Setup

The application relies on several tables within your Supabase database. You'll need to create these tables before running the application.

1.  Navigate to the SQL Editor in your Supabase project dashboard.
2.  Open the `docs/supabase_tables_creation.sql` file from this repository.
3.  Copy the contents of the file and paste them into the Supabase SQL Editor.
4.  Run the query to create all the necessary tables.

The script will create the following tables:

-   **`users`**: Stores user authentication data, such as national ID and password hash.
-   **`question_definitions`**: A lookup table containing the text for the mole symptom questionnaire.
-   **`mole_questionnaires`**: Stores users' answers to the mole questionnaire.
-   **`ham_metadata`**: Holds metadata for the HAM10000 image dataset, which is used as the reference set. It also stores pre-computed image embeddings for similarity searches.
-   **`cnn_results`**: Caches the output from the image analysis model (CNN) for each user-submitted mole image.
-   **`similar_moles_ann_user`**: Stores the results of the Approximate Nearest Neighbor (ANN) search, linking a user's mole to the three most similar moles from the HAM10000 dataset.
-   **`final_recommendation`**: Stores the final diagnostic recommendation provided to the user based on the model and questionnaire results.

## Running the Application

Once the setup is complete, you can run the application using one of the following methods.

### Manual Startup - No recommended at all!

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

#### Using `restart_servers_simple.py` - Highly Recommended!

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
