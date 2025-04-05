# MCP Cat Server

This document describes the design and implementation of the `server.py` file.

## Overview

The `server.py` file contains the main server implementation for the MCP Cat Server. It integrates the `CatManager` and `BreakReminderSystem` components and exposes them through the MCP protocol.

## Class Design

```python
class CatServer:
    def __init__(
        self,
        name: str = "MCP Cat Server",
        command_interval: int = 5,
        time_interval_minutes: int = 20
    ):
        # Initialize the server with configurable parameters
    
    def show_cat(self, index: int) -> Dict[str, Any]:
        # Show a cat image at the specified index, including break reminder metadata
    
    def show_cat_only(self, index: int) -> Dict[str, Any]:
        # Show only a cat image at the specified index, without any break reminder metadata
    
    def add_cat(self, url: str) -> Dict[str, Any]:
        # Add a cat image URL to the collection
    
    def should_take_break(self) -> Dict[str, Any]:
        # Check if it's time for a break
    
    def get_cat_resource(self, index: int) -> str:
        # Get a cat image URL by index (for resource access)
    
    def run(self, transport: str = "stdio") -> None:
        # Run the MCP server
```

## Design Decisions

### Integration of Components

The `CatServer` class integrates the `CatManager` and `BreakReminderSystem` components, providing:

1. **Cohesion**: All related functionality is grouped together.
2. **Encapsulation**: The components are encapsulated within the server.
3. **Coordination**: The server coordinates the interaction between components.

### MCP Tools and Resources

The server exposes the following MCP tools and resources:

#### Tools

1. **show_cat(index)**: Shows a cat image at the specified index, including break reminder metadata.
2. **show_cat_only(index)**: Shows only a cat image at the specified index, without any break reminder metadata.
3. **add_cat(url)**: Adds a cat image URL to the collection.
4. **should_take_break()**: Checks if it's time for a break.

#### Resources

1. **cat://{index}**: Provides direct access to cat images by index.

This design allows for both programmatic access through tools and direct access through resources.

### Break Reminder Metadata

Most tool responses include break reminder metadata (except for `show_cat_only`), which allows agents to:

1. **Know when it's time for a break**: The `should_take_break` field indicates if a break is recommended.
2. **Display the current status**: The `status` field provides detailed information about the break reminder system.
3. **Make informed decisions**: Agents can use this information to decide when and how to show cat images.

### Automatic Break Counter Reset

When a cat image is shown using either the `show_cat` or `show_cat_only` tool, the break counters are automatically reset. This ensures that:

1. **Breaks are acknowledged**: The system recognizes that a break has been taken.
2. **Fresh start**: After a break, the counters start from zero.
3. **Accurate tracking**: The system accurately tracks when the next break should be taken.

### Configurable Server Parameters

The server can be configured with:

1. **Name**: The name of the server.
2. **Command interval**: The number of commands before suggesting a break.
3. **Time interval**: The number of minutes before suggesting a break.

This allows for customization and adaptation to different user preferences.

### Transport Configuration

The `run` method allows specifying the transport to use for communication (e.g., stdio, websocket). This provides flexibility in how the server is deployed and used.

## Future Enhancements

1. **Authentication**: Add support for authenticating users.
2. **Multiple Users**: Support multiple users with separate break tracking.
3. **Persistence**: Save the state of the server between restarts.
4. **Admin Interface**: Provide an interface for administering the server.
5. **Metrics**: Collect and report metrics on server usage and break compliance.
