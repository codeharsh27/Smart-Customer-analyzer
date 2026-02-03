import unittest
import sys
import os

# This magic line helps Python find our main code from the 'tests' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import TicketAnalyzer

class TestAnalyzer(unittest.TestCase):
    def setUp(self):
        """Runs before every test. Sets up a fresh analyzer."""
        self.analyzer = TicketAnalyzer()

    def test_priority_high(self):
        """Test that 'crash' triggers High Priority."""
        category, priority = self.analyzer.analyze_ticket("The system crash on startup")
        self.assertEqual(priority, "high")
        self.assertEqual(category, "technical")

    def test_category_billing(self):
        """Test that payment issues go to Billing."""
        category, priority = self.analyzer.analyze_ticket("My payment failed yesterday")
        self.assertEqual(category, "billing")

    def test_empty_input(self):
        """Test that empty input is handled safely."""
        category, priority = self.analyzer.analyze_ticket("")
        self.assertEqual(priority, "low")

if __name__ == '__main__':
    unittest.main()
