"""
Cat Manager - Manages the storage and retrieval of cat image URLs.
"""
import json
import os
from typing import List, Optional

from config import get_cache_file_path


class CatManager:
    """
    Manages a collection of cat image URLs.
    
    This class provides functionality to add, retrieve, and list cat images.
    It uses a JSON cache file for persistence with a design that allows for
    future extension to local file system storage.
    """
    
    # Default cat images to use if no cache file exists
    DEFAULT_CAT_IMAGES = [
        "https://upload.wikimedia.org/wikipedia/commons/2/25/Siam_lilacpoint.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/15/Cat_August_2010-4.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/9/9b/Gustav_chocolate.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"
    ]
    
    def __init__(self):
        """Initialize a collection of cat image URLs from the cache file."""
        self._cat_images: List[str] = []
        self._load_from_cache()
    
    def _load_from_cache(self) -> None:
        """Load cat image URLs from the cache file."""
        cache_file_path = get_cache_file_path()
        
        try:
            # If the cache file exists, load cat images from it
            if os.path.exists(cache_file_path):
                with open(cache_file_path, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list) and all(isinstance(url, str) for url in data):
                        self._cat_images = data
                    else:
                        print(f"Invalid data format in cache file: {cache_file_path}")
                        self._initialize_with_defaults()
            else:
                # If the cache file doesn't exist, initialize with default images
                self._initialize_with_defaults()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading cache file: {e}")
            self._initialize_with_defaults()
    
    def _initialize_with_defaults(self) -> None:
        """Initialize with default cat images and save to cache file."""
        self._cat_images = self.DEFAULT_CAT_IMAGES.copy()
        self._save_to_cache()
    
    def _save_to_cache(self) -> None:
        """Save cat image URLs to the cache file."""
        cache_file_path = get_cache_file_path()
        
        try:
            # Create the directory if it doesn't exist
            cache_dir = os.path.dirname(cache_file_path)
            if cache_dir:  # Only create directory if there's a directory part
                os.makedirs(cache_dir, exist_ok=True)
            
            # Save cat images to the cache file
            with open(cache_file_path, "w") as f:
                json.dump(self._cat_images, f, indent=2)
        except IOError as e:
            print(f"Error saving cache file: {e}")
    
    def add_cat(self, url: str) -> int:
        """
        Add a cat image URL to the collection and save to cache file.
        
        Args:
            url: The URL of the cat image to add.
            
        Returns:
            The index of the added cat image.
        """
        self._cat_images.append(url)
        self._save_to_cache()
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
