"""
MCP Cat Server - A server to remind programmers to take breaks by showing cat images.
"""
import time
from typing import Dict, Any, Optional, List

from mcp.server.fastmcp import FastMCP


# Fallback to local imports when running directly
from cat_manager import CatManager
from break_reminder import BreakReminderSystem


class CatServer:
    """
    MCP server for showing cat images to remind programmers to take breaks.
    
    This server provides tools for showing and adding cat images, as well as
    checking if it's time for a break.
    """
    
    def __init__(
        self,
        name: str = "MCP Cat Server",
        command_interval: int = 5,
        time_interval_minutes: int = 20
    ):
        """
        Initialize the cat server.
        
        Args:
            name: The name of the server.
            command_interval: Number of commands before suggesting a break.
            time_interval_minutes: Minutes before suggesting a break.
        """
        self.mcp = FastMCP(name)
        self.cat_manager = CatManager()
        self.break_reminder = BreakReminderSystem(
            command_interval=command_interval,
            time_interval_minutes=time_interval_minutes
        )
        
        # Register tools
        self.mcp.tool()(self.show_cat)
        self.mcp.tool()(self.show_cat_only)
        self.mcp.tool()(self.add_cat)
        self.mcp.tool()(self.should_take_break)
        
        # Register resources
        self.mcp.resource("cat://{index}")(self.get_cat_resource)
    
    def show_cat(self, index: int) -> Dict[str, Any]:
        """
        Show a cat image at the specified index.
        
        Args:
            index: The index of the cat image to show.
            include_metadata: Whether to include break reminder metadata in the response.
                Defaults to True.
            
        Returns:
            A dictionary containing the cat image URL and optionally break reminder metadata.
        """
        # Record interaction
        self.break_reminder.record_interaction()
        
        # Get cat image URL
        cat_url = self.cat_manager.get_cat(index)
        
        # Check if it's time for a break
        should_break = self.break_reminder.should_take_break()
        
        # If showing a cat, reset the break counters
        self.break_reminder.reset_counters()
        
        # Return the cat image URL and break reminder metadata
        return {
            "cat_url": cat_url,
            "break_reminder": {
                "should_take_break": should_break,
                "status": self.break_reminder.get_status()
            }
        }
    
    def show_cat_only(self, index: int) -> str:
        """
        Show only a cat image at the specified index without metadata.
        
        Args:
            index: The index of the cat image to show.
            
        Returns:
            A string containing only the cat image URL.
        """
        # Record interaction
        self.break_reminder.record_interaction()
        
        # Get cat image URL
        cat_url = self.cat_manager.get_cat(index)
        
        # Check if it's time for a break (but don't include in response)
        should_break = self.break_reminder.should_take_break()
        
        # If showing a cat, reset the break counters
        self.break_reminder.reset_counters()
        
        # Return only the cat image URL
        return cat_url
    
    def add_cat(self, url: str) -> Dict[str, Any]:
        """
        Add a cat image URL to the collection.
        
        Args:
            url: The URL of the cat image to add.
            
        Returns:
            A dictionary containing the index of the added cat image and break reminder metadata.
        """
        # Record interaction
        self.break_reminder.record_interaction()
        
        # Add cat image URL
        index = self.cat_manager.add_cat(url)
        
        # Check if it's time for a break
        should_break = self.break_reminder.should_take_break()
        
        # Return the index and break reminder metadata
        return {
            "index": index,
            "break_reminder": {
                "should_take_break": should_break,
                "status": self.break_reminder.get_status()
            }
        }
    
    def should_take_break(self) -> Dict[str, Any]:
        """
        Check if it's time for a break.
        
        Returns:
            A dictionary containing the break reminder status.
        """
        # Record interaction
        self.break_reminder.record_interaction()
        
        # Check if it's time for a break
        should_break = self.break_reminder.should_take_break()
        
        # Return the break reminder status
        return {
            "should_take_break": should_break,
            "status": self.break_reminder.get_status()
        }
    
    def get_cat_resource(self, index: int) -> str:
        """
        Get a cat image URL by index.
        
        Args:
            index: The index of the cat image to retrieve.
            
        Returns:
            The URL of the cat image.
        """
        return self.cat_manager.get_cat(index) or "No cat image available"
    
    def run(self, transport: str = "stdio") -> None:
        """
        Run the MCP server.
        
        Args:
            transport: The transport to use for communication.
                Defaults to "stdio".
        """
        self.mcp.run(transport=transport)


def main():
    """Run the MCP cat server."""
    server = CatServer()
    server.run()


if __name__ == "__main__":
    main()
