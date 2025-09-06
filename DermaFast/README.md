# DermaFast - Full Stack Application

A full-stack application built with React + Vite, FastAPI, and Supabase.

## Project Structure

```
/frontend          # React + Vite frontend
/backend           # FastAPI backend
```

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Supabase Configuration
VITE_SUPABASE_URL=your_supabase_project_url_here
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

Get these values from your Supabase project dashboard at https://supabase.com/dashboard

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cd app
python main.py
```

The backend API will be available at http://localhost:8000
API documentation will be available at http://localhost:8000/docs

## Features

- **Frontend**: React with Vite, Tailwind CSS, Supabase authentication
- **Backend**: FastAPI with health check and placeholder auth routes
- **Database**: Supabase for user management and authentication

## Next Steps

1. Set up your Supabase project
2. Configure environment variables
3. Run both frontend and backend
4. Implement actual authentication logic in the backend
5. Add more features as needed
