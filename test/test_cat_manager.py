"""
Tests for the CatManager class.
"""
import unittest
from src.cat_manager import CatManager


class TestCatManager(unittest.TestCase):
    """Tests for the CatManager class."""
    
    def setUp(self):
        """Set up a CatManager instance for testing."""
        self.cat_manager = CatManager()
    
    def test_add_cat(self):
        """Test adding a cat image URL."""
        # Get the initial count (should be 4 default images)
        initial_count = self.cat_manager.count
        self.assertEqual(initial_count, 4)
        
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
        self.assertEqual(len(default_images), 4)
        
        # Test getting default images by index
        for i in range(4):
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
        self.assertEqual(len(default_images), 4)
        
        # Add some cat image URLs
        url1 = "https://example.com/cat1.jpg"
        url2 = "https://example.com/cat2.jpg"
        self.cat_manager.add_cat(url1)
        self.cat_manager.add_cat(url2)
        
        # Test listing
        expected_list = default_images + [url1, url2]
        self.assertEqual(self.cat_manager.list_cats(), expected_list)


if __name__ == "__main__":
    unittest.main()
