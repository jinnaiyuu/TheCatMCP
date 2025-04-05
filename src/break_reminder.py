"""
Break Reminder System - Tracks and manages break intervals for programmers.
"""
import time
from typing import Dict, Any


class BreakReminderSystem:
    """
    Tracks and manages break intervals for programmers.
    
    This class provides functionality to determine when a programmer should
    take a break based on the number of commands executed and time elapsed.
    """
    
    def __init__(
        self,
        command_interval: int = 5,
        time_interval_minutes: int = 20
    ):
        """
        Initialize the break reminder system.
        
        Args:
            command_interval: Number of commands before suggesting a break.
                Defaults to 5.
            time_interval_minutes: Minutes before suggesting a break.
                Defaults to 20.
        """
        self._command_interval = command_interval
        self._time_interval_seconds = time_interval_minutes * 60
        self._command_count = 0
        self._last_break_time = time.time()
    
    def record_interaction(self) -> None:
        """Record a user interaction to track command count."""
        self._command_count += 1
    
    def should_take_break(self) -> bool:
        """
        Determine if it's time for a break.
        
        Returns:
            True if it's time for a break, False otherwise.
        """
        # Check if enough commands have been executed
        if self._command_count >= self._command_interval:
            return True
        
        # Check if enough time has elapsed
        time_elapsed = time.time() - self._last_break_time
        if time_elapsed >= self._time_interval_seconds:
            return True
        
        return False
    
    def reset_counters(self) -> None:
        """Reset counters after a break is taken."""
        self._command_count = 0
        self._last_break_time = time.time()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the break reminder system.
        
        Returns:
            A dictionary containing the current status.
        """
        time_elapsed = time.time() - self._last_break_time
        time_remaining = max(0, self._time_interval_seconds - time_elapsed)
        
        return {
            "command_count": self._command_count,
            "command_interval": self._command_interval,
            "commands_until_break": max(0, self._command_interval - self._command_count),
            "time_elapsed_seconds": time_elapsed,
            "time_interval_seconds": self._time_interval_seconds,
            "time_remaining_seconds": time_remaining,
            "should_take_break": self.should_take_break()
        }
