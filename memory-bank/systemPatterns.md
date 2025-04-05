# MCP Cat Server System Patterns

## Architecture Overview

The MCP Cat Server follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────┐
│                CatServer                │
├─────────────────────────────────────────┤
│               FastMCP SDK               │
├───────────────────┬─────────────────────┤
│                   │                     │
│                   ▼                     ▼
│    ┌─────────────────────┐   ┌───────────────────────┐
│    │     CatManager      │   │   BreakReminderSystem │
│    └─────────────────────┘   └───────────────────────┘
└─────────────────────────────────────────────────────────┘
```

## Key Design Patterns

### Facade Pattern

The `CatServer` class acts as a facade, providing a simplified interface to the complex subsystems:

- It encapsulates the `CatManager` and `BreakReminderSystem` components.
- It exposes a clean interface through MCP tools and resources.
- It handles the coordination between components.

### Decorator Pattern

The MCP tools are implemented using Python decorators:

```python
# Register tools
self.mcp.tool()(self.show_cat)
self.mcp.tool()(self.add_cat)
self.mcp.tool()(self.should_take_break)

# Register resources
self.mcp.resource("cat://{index}")(self.get_cat_resource)
```

This pattern allows for:
- Clean separation of MCP protocol concerns from business logic
- Easy registration of tools and resources
- Maintainable and extensible code

### Observer Pattern

The break reminder system implements a form of the observer pattern:

- It observes user interactions through the `record_interaction` method.
- It tracks time elapsed since the last break.
- It notifies when it's time for a break through the `should_take_break` method.
- It provides detailed status information through the `get_status` method.

### Strategy Pattern

The break reminder system uses multiple strategies to determine when a break should be taken:

- Command count strategy: Suggest a break after a certain number of commands.
- Time elapsed strategy: Suggest a break after a certain amount of time.

This allows for flexibility in how breaks are determined and can be extended to include additional strategies in the future.

## Component Relationships

### CatServer and CatManager

- The `CatServer` creates and owns a `CatManager` instance.
- It delegates cat image management operations to the `CatManager`.
- It exposes the `CatManager` functionality through MCP tools and resources.

### CatServer and BreakReminderSystem

- The `CatServer` creates and owns a `BreakReminderSystem` instance.
- It records interactions with the `BreakReminderSystem` for each tool call.
- It checks if it's time for a break using the `BreakReminderSystem`.
- It resets the break counters when a cat image is shown.
- It includes break reminder metadata in tool responses.

## Critical Implementation Paths

### Tool Registration

```python
def __init__(self, name: str = "MCP Cat Server", ...):
    self.mcp = FastMCP(name)
    # ...
    
    # Register tools
    self.mcp.tool()(self.show_cat)
    self.mcp.tool()(self.add_cat)
    self.mcp.tool()(self.should_take_break)
    
    # Register resources
    self.mcp.resource("cat://{index}")(self.get_cat_resource)
```

### Break Determination

```python
def should_take_break(self) -> bool:
    # Check if enough commands have been executed
    if self._command_count >= self._command_interval:
        return True
    
    # Check if enough time has elapsed
    time_elapsed = time.time() - self._last_break_time
    if time_elapsed >= self._time_interval_seconds:
        return True
    
    return False
```

### Tool Response with Metadata

```python
def show_cat(self, index: int) -> Dict[str, Any]:
    # ...
    
    # Return the cat image URL and break reminder metadata
    return {
        "cat_url": cat_url,
        "break_reminder": {
            "should_take_break": should_break,
            "status": self.break_reminder.get_status()
        }
    }
```

## Extension Points

The system is designed with several extension points:

1. **Additional Tools**: New tools can be added to the `CatServer` class and registered with the MCP server.
2. **Additional Resources**: New resources can be added to the `CatServer` class and registered with the MCP server.
3. **Local File System Storage**: The `CatManager` can be extended to support local file system storage.
4. **Additional Break Strategies**: The `BreakReminderSystem` can be extended to support additional strategies for determining when a break should be taken.
5. **Persistence**: The system can be extended to persist its state between restarts.
