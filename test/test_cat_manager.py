"""
Tests for the CatManager class.
"""
import unittest
import os
import json
import tempfile
from unittest.mock import patch
from src.cat_manager import CatManager


class TestCatManager(unittest.TestCase):
    """Tests for the CatManager class."""
    
    def setUp(self):
        """Set up a CatManager instance for testing."""
        # Create a temporary directory for the cache file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cache_file_path = os.path.join(self.temp_dir.name, "test_cat_cache.json")
        
        # Patch the get_cache_file_path function to return the test cache file path
        self.patcher = patch('src.cat_manager.get_cache_file_path', return_value=self.cache_file_path)
        self.mock_get_cache_file_path = self.patcher.start()
        
        # Create a CatManager instance
        self.cat_manager = CatManager()
    
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        self.temp_dir.cleanup()
    
    def test_add_cat(self):
        """Test adding a cat image URL."""
        # Get the initial count
        initial_count = self.cat_manager.count
        
        url = "https://example.com/cat1.jpg"
        index = self.cat_manager.add_cat(url)
        self.assertEqual(index, initial_count)
        self.assertEqual(self.cat_manager.count, initial_count + 1)
        
        url2 = "https://example.com/cat2.jpg"
        index2 = self.cat_manager.add_cat(url2)
        self.assertEqual(index2, initial_count + 1)
        self.assertEqual(self.cat_manager.count, initial_count + 2)
    
    def test_get_cat(self):
        """Test getting a cat image URL by index."""
        # Get the default images
        default_images = self.cat_manager.list_cats()
        
        # Test getting default images by index
        for i in range(len(default_images)):
            self.assertEqual(self.cat_manager.get_cat(i), default_images[i])
        
        # Add some cat image URLs
        url1 = "https://example.com/cat1.jpg"
        url2 = "https://example.com/cat2.jpg"
        index1 = self.cat_manager.add_cat(url1)
        index2 = self.cat_manager.add_cat(url2)
        
        # Test getting by index
        self.assertEqual(self.cat_manager.get_cat(index1), url1)
        self.assertEqual(self.cat_manager.get_cat(index2), url2)
        
        # Test index wrapping
        total_count = self.cat_manager.count
        self.assertEqual(self.cat_manager.get_cat(index2 + total_count), url2)
        self.assertEqual(self.cat_manager.get_cat(index1 + total_count), url1)
    
    def test_list_cats(self):
        """Test listing all cat image URLs."""
        # Get the default images
        default_images = self.cat_manager.list_cats()
        
        # Add some cat image URLs
        url1 = "https://example.com/cat1.jpg"
        url2 = "https://example.com/cat2.jpg"
        self.cat_manager.add_cat(url1)
        self.cat_manager.add_cat(url2)
        
        # Test listing
        expected_list = default_images + [url1, url2]
        self.assertEqual(self.cat_manager.list_cats(), expected_list)
    
    def test_cache_file_creation(self):
        """Test that the cache file is created."""
        # Verify that the cache file exists
        self.assertTrue(os.path.exists(self.cache_file_path))
        
        # Verify that the cache file contains valid JSON
        with open(self.cache_file_path, "r") as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertTrue(all(isinstance(url, str) for url in data))
    
    def test_cache_file_persistence(self):
        """Test that cat images are persisted to the cache file."""
        # Get the initial count
        initial_count = self.cat_manager.count
        
        # Add a cat image URL
        url = "https://example.com/cat1.jpg"
        index = self.cat_manager.add_cat(url)
        
        # Verify that the cache file contains the added image
        with open(self.cache_file_path, "r") as f:
            data = json.load(f)
            self.assertEqual(len(data), initial_count + 1)
            self.assertEqual(data[index], url)
        
        # Create a new CatManager instance (which should load from the cache file)
        new_cat_manager = CatManager()
        
        # Verify that the new instance has the added image
        self.assertEqual(new_cat_manager.count, initial_count + 1)
        self.assertEqual(new_cat_manager.get_cat(index), url)
    
    def test_cache_file_error_handling(self):
        """Test error handling for corrupted cache file."""
        # Write invalid JSON to the cache file
        with open(self.cache_file_path, "w") as f:
            f.write("invalid json")
        
        # Create a new CatManager instance (which should handle the error)
        new_cat_manager = CatManager()
        
        # Verify that the instance has the default images
        self.assertEqual(new_cat_manager.count, len(CatManager.DEFAULT_CAT_IMAGES))
        self.assertEqual(new_cat_manager.list_cats(), CatManager.DEFAULT_CAT_IMAGES)
        
        # Verify that the cache file has been fixed
        with open(self.cache_file_path, "r") as f:
            data = json.load(f)
            self.assertEqual(data, CatManager.DEFAULT_CAT_IMAGES)


if __name__ == "__main__":
    unittest.main()
