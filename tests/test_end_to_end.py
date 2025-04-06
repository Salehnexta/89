import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock
import datetime

# Add the parent directory to sys.path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.mock_tools import search_mock_flights, search_mock_hotels, get_mock_general_info
from app.database import init_db, save_conversation, get_conversation


class TestEndToEnd(unittest.TestCase):
    """End-to-end tests for the AI Travel Assistant application."""

    def setUp(self):
        """Set up test environment before each test."""
        # Initialize database with test configuration
        init_db()
        
        # Create a test session ID
        self.session_id = "test_session_123"
        
    def test_database_operations(self):
        """Test basic database operations."""
        # Create test conversation history
        test_history = [
            {"role": "user", "content": "I want to travel to Paris"},
            {"role": "assistant", "content": "I can help you plan a trip to Paris. When would you like to go?"}
        ]
        
        # Save conversation to database
        save_conversation(self.session_id, test_history)
        
        # Retrieve conversation from database
        retrieved_history = get_conversation(self.session_id)
        
        # Verify data was saved and retrieved correctly
        self.assertEqual(len(retrieved_history), len(test_history))
        self.assertEqual(retrieved_history[0]["content"], test_history[0]["content"])
        self.assertEqual(retrieved_history[1]["content"], test_history[1]["content"])

    def test_mock_flight_search(self):
        """Test the mock flight search functionality."""
        # Test with basic parameters
        flights = search_mock_flights(
            destination="Paris",
            date="2025-06-15",
            return_date="2025-06-22",
            num_passengers=2,
            departure_city="New York"
        )
        
        # Verify flight results
        self.assertIsNotNone(flights)
        self.assertGreater(len(flights), 0)
        
        # Check flight details
        for flight in flights:
            self.assertIn("airline", flight)
            self.assertIn("flight_number", flight)
            self.assertIn("price", flight)
            self.assertIn("departure_time", flight)
            self.assertIn("arrival_time", flight)
            
            # Verify price calculation for 2 passengers
            self.assertGreater(flight["price"], 0)
            
        # Test filtering for morning flights
        morning_flights = [f for f in flights if "AM" in f["departure_time"] and f["stops"] == 0]
        self.assertGreater(len(morning_flights), 0)

    def test_mock_hotel_search(self):
        """Test the mock hotel search functionality."""
        # Test with basic parameters
        hotels = search_mock_hotels(
            destination="Paris",
            check_in="2025-06-15",
            check_out="2025-06-22",
            num_guests=2
        )
        
        # Verify hotel results
        self.assertIsNotNone(hotels)
        self.assertGreater(len(hotels), 0)
        
        # Check hotel details
        for hotel in hotels:
            self.assertIn("name", hotel)
            self.assertIn("rating", hotel)
            self.assertIn("price_per_night", hotel)
            self.assertIn("amenities", hotel)
        
        # Test filtering for hotels with specific amenities
        # Find amenities that actually exist in our mock data
        common_amenities = set()
        for hotel in hotels:
            if len(common_amenities) < 2 and "amenities" in hotel:
                for amenity in hotel["amenities"]:
                    common_amenities.add(amenity)
                    if len(common_amenities) >= 2:
                        break
        
        if common_amenities:
            amenities = list(common_amenities)[:2]  # Take up to 2 amenities
            filtered_hotels = search_mock_hotels(
                destination="Paris",
                check_in="2025-06-15",
                check_out="2025-06-22",
                num_guests=2,
                amenities=amenities
            )
            
            # Verify filtered results if we have any
            if filtered_hotels:
                for hotel in filtered_hotels:
                    for amenity in amenities:
                        self.assertIn(amenity, hotel["amenities"])

    def test_mock_general_info(self):
        """Test the mock general information functionality."""
        # Test weather information
        weather_info = get_mock_general_info("weather", "Paris")
        self.assertIn("weather", weather_info)
        self.assertIn("summer", weather_info["weather"])
        
        # Test attraction information
        attraction_info = get_mock_general_info("attractions", "Paris")
        self.assertIn("attractions", attraction_info)
        self.assertGreater(len(attraction_info["attractions"]), 0)
        
        # Test travel document information
        document_info = get_mock_general_info("travel documents", "Paris")
        self.assertIn("travel_documents", document_info)
        self.assertIn("visa_requirements", document_info["travel_documents"])
        
        # Test with a destination not in the database
        generic_info = get_mock_general_info("weather", "RandomCity")
        self.assertIn("weather", generic_info)
        self.assertIn("summer", generic_info["weather"])


if __name__ == '__main__':
    unittest.main()
