"""
FAISS service for Approximate Nearest Neighbor search
This module provides functionality to find similar mole images using FAISS
"""

import faiss
import numpy as np
from typing import List, Tuple, Optional
from .supabase_client import supabase_client as supabase


class FAISSService:
    def __init__(self):
        self.index = None
        self.image_ids = []
        self.embeddings_loaded = False
    
    async def load_embeddings(self) -> bool:
        """
        Load only embeddings that are not null from the ham_metadata table and build FAISS index
        """
        try:
            # Fetch only records with non-null embeddings from ham_metadata table
            response = supabase.table("ham_metadata").select("image_id, embedding").not_.is_("embedding", "null").execute()
            
            if not response.data:
                print("No embeddings found in ham_metadata table")
                return False
            
            print(f"Found {len(response.data)} records with embeddings in ham_metadata table")
            
            # Extract embeddings and image_ids
            embeddings_list = []
            image_ids_list = []
            
            for row in response.data:
                if row['embedding'] and len(row['embedding']) > 0:
                    embeddings_list.append(row['embedding'])
                    image_ids_list.append(row['image_id'])
            
            if not embeddings_list:
                print("No valid embeddings found")
                return False
            
            # Convert to numpy array
            embeddings_array = np.array(embeddings_list, dtype=np.float32)
            
            # Build FAISS index (using L2 distance)
            dimension = embeddings_array.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings_array)
            
            self.image_ids = image_ids_list
            self.embeddings_loaded = True
            
            print(f"FAISS index built with {len(embeddings_list)} embeddings of dimension {dimension}")
            return True
            
        except Exception as e:
            print(f"Error loading embeddings: {str(e)}")
            return False
    
    async def find_similar_images(self, query_embedding: List[float], k: int = 9) -> List[Tuple[str, float]]:
        """
        Find k most similar images to the query embedding
        
        Args:
            query_embedding: The embedding vector to search for
            k: Number of similar images to return (default: 9)
        
        Returns:
            List of tuples containing (image_id, distance)
        """
        try:
            # Load embeddings if not already loaded
            if not self.embeddings_loaded:
                success = await self.load_embeddings()
                if not success:
                    return []
            
            # Convert query embedding to numpy array
            query_vector = np.array([query_embedding], dtype=np.float32)
            
            # Ensure k doesn't exceed available data
            k = min(k, len(self.image_ids))
            
            # Search for similar embeddings
            distances, indices = self.index.search(query_vector, k)
            
            # Prepare results
            results = []
            for i in range(k):
                idx = indices[0][i]
                distance = float(distances[0][i])
                image_id = self.image_ids[idx]
                results.append((image_id, distance))
            
            return results
            
        except Exception as e:
            print(f"Error finding similar images: {str(e)}")
            return []
    
    async def get_image_metadata(self, image_ids: List[str]) -> List[dict]:
        """
        Get metadata for the given image IDs
        
        Args:
            image_ids: List of image IDs to get metadata for
            
        Returns:
            List of metadata dictionaries with constructed image URLs
        """
        try:
            response = supabase.table("ham_metadata").select(
                "image_id, dx, age, sex, localization"
            ).in_("image_id", image_ids).execute()
            
            if not response.data:
                return []
            
            # Use the correct, case-sensitive bucket name
            bucket_name = "HAM10000_for_comparison"
            
            # Add constructed image_url to each metadata entry
            for item in response.data:
                # Strip potential whitespace from image_id and create the path
                image_id = item['image_id'].strip()
                image_path = f"{image_id}.jpg"
                
                # Use the Supabase client to get the public URL, which is more robust
                public_url = supabase.storage.from_(bucket_name).get_public_url(image_path)
                item['image_url'] = public_url
            
            return response.data
            
        except Exception as e:
            print(f"Error getting image metadata: {str(e)}")
            return []


# Global instance
faiss_service = FAISSService()
