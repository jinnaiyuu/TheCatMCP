"""
Tests for the CatServer class.
"""
import unittest
from unittest.mock import MagicMock, patch
from src.server import CatServer


class TestCatServer(unittest.TestCase):
    """Tests for the CatServer class."""
    
    def setUp(self):
        """Set up a CatServer instance for testing."""
        # Mock the FastMCP class
        self.mock_fastmcp_patcher = patch('src.server.FastMCP')
        self.mock_fastmcp = self.mock_fastmcp_patcher.start()
        
        # Create a mock instance for the FastMCP class
        self.mock_mcp_instance = MagicMock()
        self.mock_fastmcp.return_value = self.mock_mcp_instance
        
        # Create a CatServer instance
        self.server = CatServer()
    
    def tearDown(self):
        """Clean up after tests."""
        self.mock_fastmcp_patcher.stop()
    
    def test_initialization(self):
        """Test server initialization."""
        # Verify that FastMCP was initialized with the correct name
        self.mock_fastmcp.assert_called_once_with("MCP Cat Server")
        
        # Verify that tools were registered
        self.assertEqual(self.mock_mcp_instance.tool.call_count, 4)
        
        # Verify that resources were registered
        self.assertEqual(self.mock_mcp_instance.resource.call_count, 1)
    
    def test_show_cat(self):
        """Test showing a cat image."""
        # Get the initial count of default images
        initial_count = self.server.cat_manager.count
        
        # Add a cat image URL
        url = "https://example.com/cat.jpg"
        index = self.server.cat_manager.add_cat(url)
        
        # Call show_cat with the correct index
        result = self.server.show_cat(index)
        
        # Verify the result
        self.assertEqual(result["cat_url"], url)
        self.assertIn("break_reminder", result)
        self.assertIn("should_take_break", result["break_reminder"])
        self.assertIn("status", result["break_reminder"])
        
        # Verify that the break counters were reset
        self.assertEqual(self.server.break_reminder._command_count, 0)
    
    def test_show_cat_only(self):
        """Test showing only a cat image without metadata."""
        # Get the initial count of default images
        initial_count = self.server.cat_manager.count
        
        # Add a cat image URL
        url = "https://example.com/cat.jpg"
        index = self.server.cat_manager.add_cat(url)
        
        # Call show_cat_only with the correct index
        result = self.server.show_cat_only(index)
        
        # Verify the result
        self.assertEqual(result["cat_url"], url)
        self.assertNotIn("break_reminder", result)
        
        # Verify that the break counters were reset
        self.assertEqual(self.server.break_reminder._command_count, 0)
    
    def test_add_cat(self):
        """Test adding a cat image."""
        # Get the initial count of default images
        initial_count = self.server.cat_manager.count
        
        # Call add_cat
        url = "https://example.com/cat.jpg"
        result = self.server.add_cat(url)
        
        # Verify the result
        self.assertEqual(result["index"], initial_count)
        self.assertIn("break_reminder", result)
        
        # Verify that the cat image was added
        self.assertEqual(self.server.cat_manager.count, initial_count + 1)
        self.assertEqual(self.server.cat_manager.get_cat(initial_count), url)
    
    def test_should_take_break(self):
        """Test checking if it's time for a break."""
        # Call should_take_break
        result = self.server.should_take_break()
        
        # Verify the result
        self.assertIn("should_take_break", result)
        self.assertIn("status", result)
        
        # Verify that an interaction was recorded
        self.assertEqual(self.server.break_reminder._command_count, 1)
    
    def test_get_cat_resource(self):
        """Test getting a cat image resource."""
        # Get a default cat image
        default_image = self.server.cat_manager.get_cat(0)
        
        # Test with default cat images
        result = self.server.get_cat_resource(0)
        self.assertEqual(result, default_image)
        
        # Add a cat image URL
        url = "https://example.com/cat.jpg"
        index = self.server.cat_manager.add_cat(url)
        
        # Test with the added cat image
        result = self.server.get_cat_resource(index)
        self.assertEqual(result, url)
    
    def test_run(self):
        """Test running the server."""
        # Call run
        self.server.run()
        
        # Verify that mcp.run was called with the correct transport
        self.mock_mcp_instance.run.assert_called_once_with(transport="stdio")
        
        # Test with a different transport
        self.server.run(transport="websocket")
        self.mock_mcp_instance.run.assert_called_with(transport="websocket")


if __name__ == "__main__":
    unittest.main()
