# DermaFast Backend Setup Guide

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_role_key_here

# Frontend Environment Variables (for Vite)
VITE_SUPABASE_URL=https://your-project-id.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

## Database Setup

1. Go to your Supabase project dashboard
2. Navigate to the SQL Editor
3. Run the following SQL to create the users table:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    national_id VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index on national_id for faster lookups
CREATE INDEX idx_users_national_id ON users(national_id);
```

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Running the Backend

```bash
cd backend/app
python main.py
```

The API will be available at http://localhost:8000
API documentation will be available at http://localhost:8000/docs

## API Endpoints

- `POST /api/register` - Register a new user
- `POST /api/login` - Login user
- `GET /health` - Health check
- `GET /` - API information

## Testing the API

You can test the endpoints using the interactive docs at http://localhost:8000/docs or with curl:

```bash
# Register a user
curl -X POST "http://localhost:8000/api/register" \
     -H "Content-Type: application/json" \
     -d '{"national_id": "123456789", "password": "password123"}'

# Login
curl -X POST "http://localhost:8000/api/login" \
     -H "Content-Type: application/json" \
     -d '{"national_id": "123456789", "password": "password123"}'
```
