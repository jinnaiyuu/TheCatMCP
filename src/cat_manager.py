"""
Cat Manager - Manages the storage and retrieval of cat image URLs.
"""
from typing import List, Optional


class CatManager:
    """
    Manages a collection of cat image URLs.
    
    This class provides functionality to add, retrieve, and list cat images.
    It currently supports URL-based storage with a design that allows for
    future extension to local file system storage.
    """
    
    def __init__(self):
        """Initialize a collection of cat image URLs with some default images."""
        self._cat_images: List[str] = [
            "https://upload.wikimedia.org/wikipedia/commons/2/25/Siam_lilacpoint.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/1/15/Cat_August_2010-4.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/9/9b/Gustav_chocolate.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"
        ]
    
    def add_cat(self, url: str) -> int:
        """
        Add a cat image URL to the collection.
        
        Args:
            url: The URL of the cat image to add.
            
        Returns:
            The index of the added cat image.
        """
        self._cat_images.append(url)
        return len(self._cat_images) - 1  # Return the index of the added image
    
    def get_cat(self, index: int) -> Optional[str]:
        """
        Get a cat image URL by index.
        
        If the index is out of range, it will be wrapped around using modulo.
        
        Args:
            index: The index of the cat image to retrieve.
            
        Returns:
            The URL of the cat image, or None if no images are available.
        """
        if not self._cat_images:
            return None
        
        # Use modulo to wrap around if the index is out of range
        adjusted_index = index % len(self._cat_images)
        return self._cat_images[adjusted_index]
    
    def list_cats(self) -> List[str]:
        """
        Get a list of all cat image URLs.
        
        Returns:
            A list of all cat image URLs.
        """
        return self._cat_images.copy()
    
    @property
    def count(self) -> int:
        """
        Get the number of cat images in the collection.
        
        Returns:
            The number of cat images.
        """
        return len(self._cat_images)
