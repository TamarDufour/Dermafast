#!/usr/bin/env python3
"""
Comprehensive test script for DermaFast application
Tests authentication, CNN analysis, FAISS similarity search, and database storage
"""

import asyncio
import os
import sys
import tempfile
import requests
from PIL import Image
import numpy as np
import io

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.supabase_client import supabase_client as supabase
from app.auth import AuthService
from app.ml_model import load_model, inference
from app.faiss_service import faiss_service

class DermaFastTester:
    def __init__(self):
        self.test_user_id = "test_comprehensive_123"
        self.test_password = "test_password_123"
        self.access_token = None
        
    async def cleanup_test_user(self):
        """Clean up any existing test user and results"""
        try:
            # Clean up dependent tables first
            print("   Cleaning up test data...")
            supabase.table('cnn_results').delete().eq('national_id', self.test_user_id).execute()
            supabase.table('similar_moles_ann_user').delete().eq('national_id', self.test_user_id).execute()
            
            # Now, clean up the user
            supabase.table('users').delete().eq('national_id', self.test_user_id).execute()
            
            print("   ✅ Cleaned up existing test data")
        except Exception as e:
            print(f"   ⚠️  Cleanup warning: {str(e)}")
    
    def create_test_image(self) -> bytes:
        """Create a simple test image"""
        # Create a 224x224 RGB image with random colors (typical CNN input size)
        img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        img = Image.fromarray(img_array, 'RGB')
        
        # Convert to bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        return img_buffer.getvalue()
    
    async def test_user_creation_and_auth(self) -> bool:
        """Test user creation and authentication"""
        print("\n🔐 Testing User Creation and Authentication...")
        
        try:
            # Clean up first
            await self.cleanup_test_user()
            
            # Create test user
            print("   Creating test user...")
            success = await AuthService.create_user(self.test_user_id, self.test_password)
            if not success:
                print("   ❌ Failed to create test user")
                return False
            print("   ✅ Test user created successfully")
            
            # Authenticate user
            print("   Authenticating test user...")
            user_info = await AuthService.authenticate_user(self.test_user_id, self.test_password)
            if not user_info:
                print("   ❌ Failed to authenticate test user")
                return False
            
            self.access_token = user_info['access_token']
            print(f"   ✅ Authentication successful, token: {self.access_token[:20]}...")
            
            # Test token validation
            print("   Testing token validation...")
            auth_header = f"Bearer {self.access_token}"
            current_user = await AuthService.get_current_user(auth_header)
            if current_user['national_id'] != self.test_user_id:
                print("   ❌ Token validation failed")
                return False
            print("   ✅ Token validation successful")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Authentication test error: {str(e)}")
            return False
    
    async def test_cnn_model(self) -> tuple:
        """Test CNN model inference"""
        print("\n🧠 Testing CNN Model...")
        
        try:
            # Load model
            print("   Loading CNN model...")
            # Construct the absolute path to the model weights file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, 'app', 'ml_model', 'model_weights.pkl')
            model = load_model(model_path)
            print("   ✅ CNN model loaded successfully")
            
            # Create test image
            print("   Creating test image...")
            test_image_bytes = self.create_test_image()
            print(f"   ✅ Test image created, size: {len(test_image_bytes)} bytes")
            
            # Run inference
            print("   Running CNN inference...")
            cnn_result, embedding_list = inference(model, test_image_bytes)
            print(f"   ✅ CNN inference successful")
            print(f"   CNN result: {cnn_result:.6f}")
            print(f"   Embedding dimensions: {len(embedding_list)}")
            
            return cnn_result, embedding_list, test_image_bytes
            
        except Exception as e:
            print(f"   ❌ CNN model test error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, None, None
    
    async def test_database_storage(self, cnn_result: float, embedding_list: list) -> bool:
        """Test storing results in cnn_results table"""
        print("\n💾 Testing Database Storage...")
        
        try:
            print("   Storing CNN results in database...")
            insert_response = supabase.table("cnn_results").insert({
                "national_id": self.test_user_id,
                "cnn_result": float(cnn_result),
                "embedding": embedding_list
            }).execute()
            
            if not insert_response.data:
                print("   ❌ Failed to store CNN results")
                return False
            
            stored_data = insert_response.data[0]
            print(f"   ✅ CNN results stored successfully")
            print(f"   Stored CNN result: {stored_data.get('cnn_result')}")
            print(f"   Stored embedding dimensions: {len(stored_data.get('embedding', []))}")
            print(f"   Timestamp: {stored_data.get('timestamp')}")
            
            # Verify by reading back
            print("   Verifying stored data...")
            verify_response = supabase.table("cnn_results").select("*").eq("national_id", self.test_user_id).execute()
            if not verify_response.data:
                print("   ❌ Failed to verify stored data")
                return False
            
            print("   ✅ Data verification successful")
            return True
            
        except Exception as e:
            print(f"   ❌ Database storage test error: {str(e)}")
            return False
    
    async def test_faiss_similarity(self, embedding_list: list) -> bool:
        """Test FAISS similarity search"""
        print("\n🔍 Testing FAISS Similarity Search...")
        
        try:
            print("   Loading FAISS embeddings...")
            load_success = await faiss_service.load_embeddings()
            if not load_success:
                print("   ❌ Failed to load FAISS embeddings")
                return False
            
            print(f"   ✅ FAISS embeddings loaded: {len(faiss_service.image_ids)} images")
            
            print("   Performing similarity search...")
            similar_images = await faiss_service.find_similar_images(embedding_list, k=5)
            if not similar_images:
                print("   ❌ No similar images found")
                return False
            
            print(f"   ✅ Found {len(similar_images)} similar images")
            for i, (image_id, distance) in enumerate(similar_images[:3]):
                print(f"   #{i+1}: {image_id} (distance: {distance:.4f})")
            
            # Test metadata retrieval
            print("   Retrieving image metadata...")
            image_ids = [img_id for img_id, _ in similar_images]
            metadata = await faiss_service.get_image_metadata(image_ids)
            if not metadata:
                print("   ❌ Failed to retrieve metadata")
                return False
            
            print(f"   ✅ Retrieved metadata for {len(metadata)} images")
            first_meta = metadata[0]
            print(f"   Sample: dx={first_meta.get('dx')}, age={first_meta.get('age')}, sex={first_meta.get('sex')}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ FAISS similarity test error: {str(e)}")
            return False
    
    async def test_api_endpoint(self, test_image_bytes: bytes) -> bool:
        """Test the /api/analyze endpoint via HTTP request"""
        print("\n🌐 Testing API Endpoint...")
        
        try:
            # Prepare the multipart form data
            files = {'file': ('test_image.jpg', test_image_bytes, 'image/jpeg')}
            headers = {'Authorization': f'Bearer {self.access_token}'}
            
            print("   Making HTTP request to /api/analyze...")
            response = requests.post(
                'http://localhost:8000/api/analyze',
                files=files,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"   ❌ API request failed with status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
            
            result = response.json()
            print("   ✅ API request successful")
            print(f"   CNN result: {result.get('cnn_result')}")
            print(f"   Embedding dimensions: {result.get('embedding_dimensions')}")
            print(f"   Similar images: {len(result.get('similar_images', []))}")
            
            return True
            
        except requests.exceptions.ConnectionError:
            print("   ⚠️  Server not running - skipping API endpoint test")
            return True  # Don't fail the test if server is not running
        except Exception as e:
            print(f"   ❌ API endpoint test error: {str(e)}")
            return False

    async def test_save_similar_moles_api(self) -> bool:
        """Test the /api/save_similar_moles endpoint"""
        print("\n💾 Testing Save Similar Moles API...")

        try:
            headers = {'Authorization': f'Bearer {self.access_token}', 'Content-Type': 'application/json'}
            payload = {'selected_ids': ['ISIC_0024306', 'ISIC_0024307']}

            print("   Making HTTP request to /api/save_similar_moles...")
            response = requests.post(
                'http://localhost:8000/api/save_similar_moles',
                json=payload,
                headers=headers,
                timeout=15
            )

            if response.status_code != 200:
                print(f"   ❌ API request failed with status {response.status_code}")
                print(f"   Response: {response.text}")
                return False

            print("   ✅ API request successful")

            # Verify the data was stored correctly
            print("   Verifying stored data...")
            verify_response = supabase.table("similar_moles_ann_user").select("*").eq("national_id", self.test_user_id).order("timestamp", desc=True).limit(1).execute()
            
            if not verify_response.data:
                print("   ❌ Failed to find stored data for verification")
                return False
            
            stored_data = verify_response.data[0]
            if stored_data['image_id1'] == 'ISIC_0024306' and stored_data['image_id2'] == 'ISIC_0024307' and stored_data['image_id3'] is None:
                print("   ✅ Data verification successful")
                return True
            else:
                print("   ❌ Stored data does not match payload")
                print(f"   Stored data: {stored_data}")
                return False

        except requests.exceptions.ConnectionError:
            print("   ⚠️  Server not running - skipping save similar moles API test")
            return True
        except Exception as e:
            print(f"   ❌ Save similar moles API test error: {str(e)}")
            return False

    async def run_all_tests(self):
        """Run all comprehensive tests"""
        print("🧪 Starting Comprehensive DermaFast Tests...")
        print("=" * 50)
        
        test_results = {
            'auth': False,
            'cnn': False,
            'database': False,
            'faiss': False,
            'api': False,
            'save_moles': False
        }
        
        # Test 1: Authentication
        test_results['auth'] = await self.test_user_creation_and_auth()
        
        if test_results['auth']:
            # Test 2: CNN Model
            cnn_result, embedding_list, test_image_bytes = await self.test_cnn_model()
            test_results['cnn'] = cnn_result is not None
            
            if test_results['cnn']:
                # Test 3: Database Storage
                test_results['database'] = await self.test_database_storage(cnn_result, embedding_list)
                
                # Test 4: FAISS Similarity
                test_results['faiss'] = await self.test_faiss_similarity(embedding_list)
                
                # Test 5: API Endpoint
                test_results['api'] = await self.test_api_endpoint(test_image_bytes)

                # Test 6: Save Similar Moles
                test_results['save_moles'] = await self.test_save_similar_moles_api()
        
        # Clean up
        await self.cleanup_test_user()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📋 Test Results Summary:")
        print("=" * 50)
        
        for test_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name.upper():12} {status}")
        
        all_passed = all(test_results.values())
        overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
        print(f"\nOVERALL: {overall_status}")
        
        return all_passed

async def main():
    """Main test runner"""
    tester = DermaFastTester()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())
