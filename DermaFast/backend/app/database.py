import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
        self.connection = None
    
    async def connect(self):
        """Connect to Supabase PostgreSQL database"""
        if not self.supabase_url or not self.supabase_service_key:
            raise ValueError("Missing Supabase environment variables")
        
        # Extract database URL from Supabase URL
        # Supabase URL format: https://project.supabase.co
        # Database URL format: postgresql://postgres:[password]@db.project.supabase.co:5432/postgres
        db_url = self.supabase_url.replace("https://", "postgresql://postgres:")
        db_url = db_url.replace(".supabase.co", f":{self.supabase_service_key}@db.supabase.co:5432/postgres")
        
        self.connection = await asyncpg.connect(db_url)
    
    async def disconnect(self):
        """Disconnect from database"""
        if self.connection:
            await self.connection.close()
    
    async def execute_query(self, query: str, *args):
        """Execute a query and return results"""
        if not self.connection:
            await self.connect()
        
        return await self.connection.fetch(query, *args)
    
    async def execute_one(self, query: str, *args):
        """Execute a query and return one result"""
        if not self.connection:
            await self.connect()
        
        return await self.connection.fetchrow(query, *args)
    
    async def execute_insert(self, query: str, *args):
        """Execute an insert query"""
        if not self.connection:
            await self.connect()
        
        return await self.connection.execute(query, *args)

# Global database instance
db = Database()
