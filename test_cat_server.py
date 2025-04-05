"""
Test script for the MCP Cat Server.
"""
import sys
import time
from mcp.client import Client


def main():
    """Test the MCP Cat Server."""
    print("Connecting to MCP Cat Server...")
    client = Client()
    
    # Connect to the server
    try:
        client.connect()
        print("Connected to MCP Cat Server.")
    except Exception as e:
        print(f"Failed to connect to MCP Cat Server: {e}")
        sys.exit(1)
    
    # List available tools
    try:
        tools = client.list_tools()
        print(f"Available tools: {[tool.name for tool in tools]}")
    except Exception as e:
        print(f"Failed to list tools: {e}")
        sys.exit(1)
    
    # Show all default cat images
    try:
        for i in range(4):  # We have 4 default images
            result = client.call_tool("show_cat", {"index": i})
            print(f"Showing cat image at index {i}")
            print(f"Cat URL: {result['cat_url']}")
    except Exception as e:
        print(f"Failed to show cat image: {e}")
        sys.exit(1)
    
    # Add a new cat image URL
    try:
        cat_url = "https://placekitten.com/200/300"
        result = client.call_tool("add_cat", {"url": cat_url})
        print(f"Added cat image URL: {cat_url}")
        print(f"Index: {result['index']}")
        
        # Show the newly added cat image
        result = client.call_tool("show_cat", {"index": result['index']})
        print(f"Showing newly added cat image")
        print(f"Cat URL: {result['cat_url']}")
    except Exception as e:
        print(f"Failed to add or show cat image: {e}")
        sys.exit(1)
    
    # Check if it's time for a break
    try:
        result = client.call_tool("should_take_break", {})
        print(f"Checking if it's time for a break")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed to check if it's time for a break: {e}")
        sys.exit(1)
    
    # Record some interactions and check again
    print("Recording some interactions...")
    for i in range(5):
        try:
            result = client.call_tool("should_take_break", {})
            print(f"Interaction {i+1}: {result['should_take_break']}")
        except Exception as e:
            print(f"Failed to check if it's time for a break: {e}")
            sys.exit(1)
    
    # Wait for some time and check again
    print("Waiting for 5 seconds...")
    time.sleep(5)
    try:
        result = client.call_tool("should_take_break", {})
        print(f"After waiting: {result['should_take_break']}")
    except Exception as e:
        print(f"Failed to check if it's time for a break: {e}")
        sys.exit(1)
    
    print("Test completed successfully.")


if __name__ == "__main__":
    main()
