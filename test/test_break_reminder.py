"""
Tests for the BreakReminderSystem class.
"""
import unittest
import time
from src.break_reminder import BreakReminderSystem


class TestBreakReminderSystem(unittest.TestCase):
    """Tests for the BreakReminderSystem class."""
    
    def setUp(self):
        """Set up a BreakReminderSystem instance for testing."""
        # Use small values for testing
        self.command_interval = 3
        self.time_interval_seconds = 2
        self.break_reminder = BreakReminderSystem(
            command_interval=self.command_interval,
            time_interval_minutes=self.time_interval_seconds / 60  # Convert to minutes
        )
    
    def test_record_interaction(self):
        """Test recording a user interaction."""
        initial_count = self.break_reminder._command_count
        self.break_reminder.record_interaction()
        self.assertEqual(self.break_reminder._command_count, initial_count + 1)
    
    def test_should_take_break_command_count(self):
        """Test should_take_break based on command count."""
        # Initially should not take a break
        self.assertFalse(self.break_reminder.should_take_break())
        
        # Record interactions up to the threshold
        for _ in range(self.command_interval - 1):
            self.break_reminder.record_interaction()
        
        # Still should not take a break
        self.assertFalse(self.break_reminder.should_take_break())
        
        # Record one more interaction to reach the threshold
        self.break_reminder.record_interaction()
        
        # Now should take a break
        self.assertTrue(self.break_reminder.should_take_break())
    
    def test_should_take_break_time_elapsed(self):
        """Test should_take_break based on time elapsed."""
        # Initially should not take a break
        self.assertFalse(self.break_reminder.should_take_break())
        
        # Wait for the time interval to elapse
        time.sleep(self.time_interval_seconds + 0.1)
        
        # Now should take a break
        self.assertTrue(self.break_reminder.should_take_break())
    
    def test_reset_counters(self):
        """Test resetting counters after a break."""
        # Record interactions and wait for time to elapse
        for _ in range(self.command_interval):
            self.break_reminder.record_interaction()
        
        # Verify that a break is needed
        self.assertTrue(self.break_reminder.should_take_break())
        
        # Reset counters
        self.break_reminder.reset_counters()
        
        # Verify that a break is no longer needed
        self.assertFalse(self.break_reminder.should_take_break())
        self.assertEqual(self.break_reminder._command_count, 0)
    
    def test_get_status(self):
        """Test getting the current status."""
        # Record some interactions
        self.break_reminder.record_interaction()
        self.break_reminder.record_interaction()
        
        # Get status
        status = self.break_reminder.get_status()
        
        # Verify status fields
        self.assertEqual(status["command_count"], 2)
        self.assertEqual(status["command_interval"], self.command_interval)
        self.assertEqual(status["commands_until_break"], self.command_interval - 2)
        self.assertFalse(status["should_take_break"])


if __name__ == "__main__":
    unittest.main()
