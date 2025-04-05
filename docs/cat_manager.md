# Cat Manager

This document describes the design and implementation of the `cat_manager.py` file.

## Overview

The `CatManager` class is responsible for managing a collection of cat image URLs. It provides functionality to add, retrieve, and list cat images.

## Class Design

```python
class CatManager:
    def __init__(self):
        self._cat_images: List[str] = [
            "https://upload.wikimedia.org/wikipedia/commons/2/25/Siam_lilacpoint.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/1/15/Cat_August_2010-4.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/9/9b/Gustav_chocolate.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"
        ]
    
    def add_cat(self, url: str) -> int:
        # Add a cat image URL and return its index
    
    def get_cat(self, index: int) -> Optional[str]:
        # Get a cat image URL by index (with modulo handling)
    
    def list_cats(self) -> List[str]:
        # Get a list of all cat image URLs
    
    @property
    def count(self) -> int:
        # Get the number of cat images
```

## Design Decisions

### Default Cat Images

The `CatManager` is initialized with a set of default cat images from Wikipedia:

1. **Siamese Cat**: A lilac point Siamese cat.
2. **Tabby Cat**: A gray tabby cat.
3. **Chocolate Cat**: A chocolate-colored cat named Gustav.
4. **Orange Tabby**: An orange tabby cat sitting on fallen leaves.

This provides users with a set of cat images to start with, without having to add their own.

### URL-Based Storage

The initial implementation uses URL-based storage for cat images. This allows for:

1. **Simplicity**: URLs are easy to store and retrieve.
2. **Flexibility**: Images can be sourced from anywhere on the web.
3. **Efficiency**: No need to handle file uploads or storage.

The design allows for future extension to support local file system storage if needed.

### Index-Based Access

Cat images are accessed by index, which provides:

1. **Simplicity**: Indexes are easy to work with and understand.
2. **Predictability**: The first image added is at index 0, the second at index 1, etc.
3. **Compatibility**: Indexes work well with the MCP protocol.

### Modulo Handling for Indexes

If an index is out of range, it is wrapped around using modulo. This ensures that:

1. **No errors**: The system never fails due to an invalid index.
2. **Cycling**: Users can cycle through all available cat images.
3. **Simplicity**: No need for complex error handling.

### Defensive Copy for List Cats

The `list_cats` method returns a copy of the internal list to prevent external code from modifying the list directly. This ensures:

1. **Encapsulation**: The internal state is protected.
2. **Thread safety**: No race conditions when multiple threads access the list.
3. **Predictability**: The behavior of the class is more predictable.

## Future Enhancements

1. **Local File System Storage**: Add support for storing cat images locally.
2. **Image Metadata**: Store additional information about each image (e.g., description, tags).
3. **Persistence**: Save the collection to disk so it persists between server restarts.
4. **Categories**: Allow categorizing cat images (e.g., funny, cute, sleepy).
5. **Search**: Add functionality to search for cat images by metadata.
