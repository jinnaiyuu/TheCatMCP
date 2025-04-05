# MCP Cat Server Technical Context

## Technologies Used

### Core Technologies

- **Python**: The primary programming language used for implementation.
- **Model Context Protocol (MCP)**: The protocol used for communication between agents and the server.
- **FastMCP SDK**: The Python SDK for implementing MCP servers.

### Development Tools

- **unittest**: The testing framework used for unit tests.
- **typing**: Used for type hints to improve code readability and maintainability.
- **time**: Used for tracking time elapsed since the last break.

## Development Setup

### Prerequisites

- Python 3.6 or higher
- MCP SDK (version 1.5.0 or higher)

### Project Structure

```
mcp-cat/
├── src/                  # Source code
│   ├── __init__.py
│   ├── server.py         # Main server implementation
│   ├── cat_manager.py    # Cat image URL management
│   └── break_reminder.py # Break reminder system
├── test/                 # Unit tests
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_cat_manager.py
│   └── test_break_reminder.py
├── docs/                 # Documentation
│   ├── design.md         # Overall design decisions
│   ├── server.md         # Server implementation details
│   ├── cat_manager.md    # Cat manager implementation details
│   └── break_reminder.md # Break reminder system details
└── memory-bank/          # Memory bank for Cline
    ├── projectbrief.md
    ├── productContext.md
    ├── systemPatterns.md
    ├── techContext.md
    ├── activeContext.md
    └── progress.md
```

## Technical Constraints

### MCP SDK Constraints

- The MCP SDK requires tools to be registered using decorators.
- Resources are defined using URI templates.
- The server must be run with a specified transport (e.g., stdio, websocket).

### URL-Based Storage Constraints

- Cat images are stored as URLs, not as local files.
- The system relies on external image hosting.
- URLs must be valid and accessible.

### Break Reminder Constraints

- Command count and time elapsed are tracked in memory.
- State is not persisted between server restarts.
- Break intervals are configurable but fixed at server startup.

## Dependencies

### Direct Dependencies

- **mcp**: The MCP SDK for implementing MCP servers.
- **typing**: For type hints.
- **time**: For tracking time elapsed.
- **unittest**: For unit tests.

### Indirect Dependencies

- **pydantic**: Used by the MCP SDK for data validation.
- **asyncio**: Used by the MCP SDK for asynchronous communication.

## Tool Usage Patterns

### Running the Server

```bash
python -m src.server
```

### Running Tests

```bash
python -m unittest discover test
```

### Using the Server with an Agent

Agents can use the server by connecting to it using the MCP protocol. The server provides the following tools:

- `show_cat(index)`: Shows a cat image at the specified index.
- `add_cat(url)`: Adds a cat image URL to the collection.
- `should_take_break()`: Checks if it's time for a break.

And the following resources:

- `cat://{index}`: Provides direct access to cat images by index.

## Future Technical Considerations

### Local File System Storage

To support local file system storage, the `CatManager` class would need to be extended to:

- Accept file paths or file objects.
- Store files in a designated directory.
- Return file paths or URLs to local files.

### Persistence

To support persistence, the system would need to:

- Serialize the state of the `CatManager` and `BreakReminderSystem` to disk.
- Load the state from disk on startup.
- Handle errors and edge cases (e.g., missing files, corrupt data).

### Multiple Users

To support multiple users, the system would need to:

- Track state per user.
- Identify users (e.g., using session IDs or authentication).
- Store and retrieve user-specific data.
