"""Mock tools for the AI Travel Assistant demo."""
from typing import List, Dict, Any
from datetime import datetime, timedelta

def search_mock_flights(
    destination: str,
    date: str,
    return_date: str = None,
    num_passengers: int = 1,
    departure_city: str = "New York"
) -> List[Dict[str, Any]]:
    """Mock flight search function with realistic data."""
    # Base prices vary by destination
    destination_prices = {
        "Paris": 799.99,
        "London": 749.99,
        "Tokyo": 1299.99,
        "Rome": 849.99,
        "Barcelona": 899.99,
        "Dubai": 1099.99,
        "Sydney": 1599.99,
        "Bangkok": 1199.99,
        "Singapore": 1299.99,
        "New York": 399.99,
    }
    
    # Default price if destination not in our list
    base_price = destination_prices.get(destination, 899.99)
    
    # Airlines and their codes
    airlines = [
        {"name": "Air France", "code": "AF"},
        {"name": "Delta Airlines", "code": "DL"},
        {"name": "British Airways", "code": "BA"},
        {"name": "Lufthansa", "code": "LH"},
        {"name": "Emirates", "code": "EK"},
        {"name": "United Airlines", "code": "UA"},
        {"name": "American Airlines", "code": "AA"},
        {"name": "Qatar Airways", "code": "QR"},
        {"name": "Singapore Airlines", "code": "SQ"},
    ]
    
    # Morning flights
    morning_flights = [
        {
            "airline": airlines[0]["name"],
            "airline_code": airlines[0]["code"],
            "flight_number": f"{airlines[0]['code']}1234",
            "departure_city": departure_city,
            "destination_city": destination,
            "departure_time": "07:30 AM",
            "arrival_time": "10:45 AM",
            "duration": "8h 15m",
            "price": round(base_price * 1.1 * num_passengers, 2),
            "seats_available": 8,
            "cabin_class": "Economy",
            "stops": 0,
            "aircraft": "Boeing 787-9",
            "amenities": ["Wi-Fi", "In-seat power", "On-demand entertainment"],
            "baggage_allowance": "1 carry-on, 1 checked bag",
            "refundable": False,
            "departure_date": date,
            "return_date": return_date
        },
        {
            "airline": airlines[1]["name"],
            "airline_code": airlines[1]["code"],
            "flight_number": f"{airlines[1]['code']}5678",
            "departure_city": departure_city,
            "destination_city": destination,
            "departure_time": "08:45 AM",
            "arrival_time": "12:30 PM",
            "duration": "8h 45m",
            "price": round(base_price * 0.9 * num_passengers, 2),
            "seats_available": 12,
            "cabin_class": "Economy",
            "stops": 1,
            "stopover_city": "London",
            "stopover_duration": "1h 30m",
            "aircraft": "Airbus A330-300",
            "amenities": ["Wi-Fi", "In-seat power"],
            "baggage_allowance": "1 carry-on, 1 checked bag",
            "refundable": False,
            "departure_date": date,
            "return_date": return_date
        },
    ]
    
    # Afternoon flights
    afternoon_flights = [
        {
            "airline": airlines[2]["name"],
            "airline_code": airlines[2]["code"],
            "flight_number": f"{airlines[2]['code']}9012",
            "departure_city": departure_city,
            "destination_city": destination,
            "departure_time": "1:15 PM",
            "arrival_time": "9:30 PM",
            "duration": "8h 15m",
            "price": round(base_price * 0.95 * num_passengers, 2),
            "seats_available": 6,
            "cabin_class": "Economy",
            "stops": 0,
            "aircraft": "Boeing 777-300ER",
            "amenities": ["Wi-Fi", "In-seat power", "On-demand entertainment", "Complimentary meal"],
            "baggage_allowance": "1 carry-on, 1 checked bag",
            "refundable": True,
            "refund_fee": "$150",
            "departure_date": date,
            "return_date": return_date
        },
    ]
    
    # Evening flights
    evening_flights = [
        {
            "airline": airlines[3]["name"],
            "airline_code": airlines[3]["code"],
            "flight_number": f"{airlines[3]['code']}3456",
            "departure_city": departure_city,
            "destination_city": destination,
            "departure_time": "6:30 PM",
            "arrival_time": "8:45 AM",
            "duration": "9h 15m",
            "price": round(base_price * 0.85 * num_passengers, 2),
            "seats_available": 15,
            "cabin_class": "Economy",
            "stops": 0,
            "aircraft": "Airbus A350-900",
            "amenities": ["Wi-Fi", "In-seat power", "On-demand entertainment"],
            "baggage_allowance": "1 carry-on, 1 checked bag",
            "refundable": False,
            "departure_date": date,
            "return_date": return_date
        },
    ]
    
    # Premium flights
    premium_flights = [
        {
            "airline": airlines[4]["name"],
            "airline_code": airlines[4]["code"],
            "flight_number": f"{airlines[4]['code']}7890",
            "departure_city": departure_city,
            "destination_city": destination,
            "departure_time": "10:00 AM",
            "arrival_time": "6:15 PM",
            "duration": "8h 15m",
            "price": round(base_price * 2.5 * num_passengers, 2),
            "seats_available": 4,
            "cabin_class": "Business",
            "stops": 0,
            "aircraft": "Boeing 787-10",
            "amenities": ["Wi-Fi", "Lie-flat seats", "Premium dining", "Lounge access", "Priority boarding"],
            "baggage_allowance": "2 carry-on, 2 checked bags",
            "refundable": True,
            "departure_date": date,
            "return_date": return_date
        },
    ]
    
    # Combine all flights
    mock_flights = morning_flights + afternoon_flights + evening_flights + premium_flights
    
    return mock_flights

def search_mock_hotels(
    destination: str,
    check_in: str,
    check_out: str = None,
    num_guests: int = 1,
    neighborhood: str = None,
    amenities: List[str] = None
) -> List[Dict[str, Any]]:
    """Mock hotel search function with realistic data."""
    # Base prices vary by destination
    destination_prices = {
        "Paris": 249.99,
        "London": 279.99,
        "Tokyo": 229.99,
        "Rome": 199.99,
        "Barcelona": 189.99,
        "Dubai": 299.99,
        "Sydney": 219.99,
        "Bangkok": 129.99,
        "Singapore": 239.99,
        "New York": 329.99,
    }
    
    # Default price if destination not in our list
    base_price = destination_prices.get(destination, 199.99)
    
    # City-specific neighborhoods
    neighborhoods = {
        "Paris": ["Le Marais", "Saint-Germain-des-Prés", "Montmartre", "Champs-Élysées", "Latin Quarter"],
        "London": ["Westminster", "Kensington", "Covent Garden", "Shoreditch", "Camden"],
        "Tokyo": ["Shinjuku", "Shibuya", "Ginza", "Asakusa", "Roppongi"],
        "New York": ["Midtown", "SoHo", "Upper East Side", "Greenwich Village", "Times Square"],
    }
    
    # Get neighborhoods for the destination or use generic ones
    city_neighborhoods = neighborhoods.get(destination, ["Downtown", "Historic Center", "Waterfront", "Business District", "Entertainment District"])
    
    # Filter by neighborhood if specified
    if neighborhood and neighborhood in city_neighborhoods:
        selected_neighborhoods = [neighborhood]
    else:
        selected_neighborhoods = city_neighborhoods
    
    # City-specific landmarks
    landmarks = {
        "Paris": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Arc de Triomphe"],
        "London": ["Big Ben", "Buckingham Palace", "London Eye", "Tower Bridge"],
        "Tokyo": ["Tokyo Tower", "Imperial Palace", "Senso-ji Temple", "Tokyo Skytree"],
        "New York": ["Empire State Building", "Central Park", "Statue of Liberty", "Times Square"],
    }
    
    # Get landmarks for the destination or use generic ones
    city_landmarks = landmarks.get(destination, ["City Center", "Main Square", "Historic Monument", "Cultural District"])
    
    # Luxury hotels
    luxury_hotels = [
        {
            "name": f"The {destination} Grand Palace",
            "rating": 4.8,
            "price_per_night": round(base_price * 2.5 * (1 + (num_guests * 0.15)), 2),
            "neighborhood": selected_neighborhoods[0],
            "address": f"1 Luxury Avenue, {selected_neighborhoods[0]}, {destination}",
            "distance_to_center": "0.5 km",
            "nearby_landmarks": [city_landmarks[0]],
            "amenities": ["5-Star Restaurant", "Luxury Spa", "Rooftop Pool", "Concierge Service", "Free High-Speed WiFi", "Fitness Center", "Room Service", "Business Center", "Airport Shuttle"],
            "room_types": [
                {
                    "name": "Deluxe Suite",
                    "beds": "1 King Bed",
                    "size": "55 sq m",
                    "view": "City View",
                    "price": round(base_price * 2.5 * (1 + (num_guests * 0.15)), 2),
                    "available": 3
                }
            ],
            "breakfast_included": True,
            "free_cancellation": True,
            "review_count": 1245,
            "images": ["luxury_exterior.jpg", "luxury_room.jpg", "luxury_bathroom.jpg", "luxury_restaurant.jpg"],
            "check_in": check_in,
            "check_out": check_out
        },
        {
            "name": f"{destination} Royal Hotel & Spa",
            "rating": 4.9,
            "price_per_night": round(base_price * 3.0 * (1 + (num_guests * 0.15)), 2),
            "neighborhood": selected_neighborhoods[1],
            "address": f"25 Royal Boulevard, {selected_neighborhoods[1]}, {destination}",
            "distance_to_center": "1.2 km",
            "nearby_landmarks": [city_landmarks[1]],
            "amenities": ["Michelin-Star Restaurant", "Full-Service Spa", "Indoor and Outdoor Pools", "24/7 Concierge", "Free Ultra-Fast WiFi", "Premium Fitness Center", "24-Hour Room Service", "Business Lounge", "Valet Parking", "Childcare Services"],
            "room_types": [
                {
                    "name": "Executive Suite",
                    "beds": "1 King Bed",
                    "size": "65 sq m",
                    "view": "Landmark View",
                    "price": round(base_price * 3.0 * (1 + (num_guests * 0.15)), 2),
                    "available": 2
                }
            ],
            "breakfast_included": True,
            "free_cancellation": True,
            "review_count": 879,
            "images": ["royal_exterior.jpg", "royal_room.jpg", "royal_spa.jpg", "royal_restaurant.jpg"],
            "check_in": check_in,
            "check_out": check_out
        }
    ]
    
    # Mid-range hotels
    mid_range_hotels = [
        {
            "name": f"{destination} Plaza Hotel",
            "rating": 4.3,
            "price_per_night": round(base_price * 1.2 * (1 + (num_guests * 0.15)), 2),
            "neighborhood": selected_neighborhoods[2],
            "address": f"123 Main Street, {selected_neighborhoods[2]}, {destination}",
            "distance_to_center": "1.8 km",
            "nearby_landmarks": [city_landmarks[2]],
            "amenities": ["Restaurant", "Bar", "Swimming Pool", "Free WiFi", "Fitness Center", "Room Service", "Business Center"],
            "room_types": [
                {
                    "name": "Standard Double Room",
                    "beds": "1 Queen Bed",
                    "size": "28 sq m",
                    "view": "City View",
                    "price": round(base_price * 1.2 * (1 + (num_guests * 0.15)), 2),
                    "available": 8
                }
            ],
            "breakfast_included": True,
            "free_cancellation": True,
            "review_count": 2156,
            "images": ["plaza_exterior.jpg", "plaza_room.jpg", "plaza_restaurant.jpg", "plaza_pool.jpg"],
            "check_in": check_in,
            "check_out": check_out
        },
        {
            "name": f"Boutique Hotel {destination}",
            "rating": 4.5,
            "price_per_night": round(base_price * 1.4 * (1 + (num_guests * 0.15)), 2),
            "neighborhood": selected_neighborhoods[3],
            "address": f"45 Boutique Street, {selected_neighborhoods[3]}, {destination}",
            "distance_to_center": "2.1 km",
            "nearby_landmarks": [city_landmarks[3]],
            "amenities": ["Café", "Terrace", "Free WiFi", "Bicycle Rental", "Concierge Service", "Airport Shuttle"],
            "room_types": [
                {
                    "name": "Deluxe Room",
                    "beds": "1 Queen Bed",
                    "size": "32 sq m",
                    "view": "Street View",
                    "price": round(base_price * 1.4 * (1 + (num_guests * 0.15)), 2),
                    "available": 5
                }
            ],
            "breakfast_included": True,
            "free_cancellation": False,
            "review_count": 1087,
            "images": ["boutique_exterior.jpg", "boutique_room.jpg", "boutique_cafe.jpg", "boutique_terrace.jpg"],
            "check_in": check_in,
            "check_out": check_out
        }
    ]
    
    # Budget hotels
    budget_hotels = [
        {
            "name": f"{destination} Comfort Inn",
            "rating": 3.8,
            "price_per_night": round(base_price * 0.7 * (1 + (num_guests * 0.15)), 2),
            "neighborhood": selected_neighborhoods[4],
            "address": f"789 Budget Road, {selected_neighborhoods[4]}, {destination}",
            "distance_to_center": "3.5 km",
            "nearby_landmarks": [],
            "amenities": ["Free WiFi", "Breakfast Buffet", "24-Hour Reception", "Vending Machines"],
            "room_types": [
                {
                    "name": "Standard Twin Room",
                    "beds": "2 Single Beds",
                    "size": "22 sq m",
                    "view": "City View",
                    "price": round(base_price * 0.7 * (1 + (num_guests * 0.15)), 2),
                    "available": 12
                }
            ],
            "breakfast_included": True,
            "free_cancellation": False,
            "review_count": 3241,
            "images": ["comfort_exterior.jpg", "comfort_room.jpg", "comfort_breakfast.jpg", "comfort_reception.jpg"],
            "check_in": check_in,
            "check_out": check_out
        }
    ]
    
    # Combine all hotels
    all_hotels = luxury_hotels + mid_range_hotels + budget_hotels
    
    # Filter by amenities if specified
    if amenities:
        filtered_hotels = []
        for hotel in all_hotels:
            if all(amenity in hotel["amenities"] for amenity in amenities):
                filtered_hotels.append(hotel)
        return filtered_hotels
    
    return all_hotels

def get_mock_general_info(topic: str, destination: str) -> Dict[str, Any]:
    """Mock general information about destinations with realistic data."""
    # Destination-specific information
    destination_info = {
        "Paris": {
            "weather": {
                "spring": {
                    "description": "Mild and pleasant with occasional showers",
                    "temperature": "10°C - 20°C",
                    "precipitation": "Moderate",
                    "best_activities": ["Visiting gardens", "Outdoor cafés", "Walking tours"]
                },
                "summer": {
                    "description": "Warm and sunny with occasional heat waves",
                    "temperature": "18°C - 30°C",
                    "precipitation": "Low",
                    "best_activities": ["Picnics by the Seine", "Outdoor festivals", "Evening boat tours"]
                },
                "fall": {
                    "description": "Cool and crisp with beautiful foliage",
                    "temperature": "8°C - 18°C",
                    "precipitation": "Moderate",
                    "best_activities": ["Museum visits", "Food tours", "Photography walks"]
                },
                "winter": {
                    "description": "Cold with occasional snow, festive atmosphere",
                    "temperature": "1°C - 8°C",
                    "precipitation": "Moderate",
                    "best_activities": ["Christmas markets", "Indoor museums", "Cozy cafés"]
                }
            },
            "attractions": [
                {
                    "name": "Eiffel Tower",
                    "description": "Iconic 330m-tall iron tower with restaurants and observation decks",
                    "rating": 4.7,
                    "price": "€17.10 - €26.80",
                    "hours": "9:00 AM - 11:45 PM",
                    "address": "Champ de Mars, 5 Avenue Anatole France",
                    "tips": "Book tickets online to avoid long queues. Visit at sunset for spectacular views.",
                    "crowd_level": "High"
                },
                {
                    "name": "Louvre Museum",
                    "description": "World's largest art museum and historic monument housing the Mona Lisa",
                    "rating": 4.8,
                    "price": "€17",
                    "hours": "9:00 AM - 6:00 PM, Closed on Tuesdays",
                    "address": "Rue de Rivoli",
                    "tips": "Enter through the Carrousel du Louvre entrance to avoid long lines. Visit on Wednesday or Friday evening for smaller crowds.",
                    "crowd_level": "Very High"
                },
                {
                    "name": "Notre-Dame Cathedral",
                    "description": "Medieval Catholic cathedral known for its French Gothic architecture",
                    "rating": 4.7,
                    "price": "Free (exterior viewing only due to reconstruction)",
                    "hours": "Viewable 24/7 from exterior",
                    "address": "6 Parvis Notre-Dame - Pl. Jean-Paul II",
                    "tips": "The cathedral is under reconstruction after the 2019 fire, but the exterior is still worth seeing.",
                    "crowd_level": "Moderate"
                },
                {
                    "name": "Montmartre and Sacré-Cœur",
                    "description": "Historic hilltop district with artist square and stunning basilica",
                    "rating": 4.6,
                    "price": "Free (Basilica), €6 for dome access",
                    "hours": "Basilica: 6:00 AM - 10:30 PM",
                    "address": "35 Rue du Chevalier de la Barre",
                    "tips": "Visit early morning to avoid crowds. Take the funicular if you don't want to climb the steps.",
                    "crowd_level": "High"
                },
                {
                    "name": "Musée d'Orsay",
                    "description": "Museum housed in former railway station, featuring impressionist masterpieces",
                    "rating": 4.8,
                    "price": "€16",
                    "hours": "9:30 AM - 6:00 PM, Late night on Thursdays until 9:45 PM, Closed on Mondays",
                    "address": "1 Rue de la Légion d'Honneur",
                    "tips": "Thursday evenings are less crowded. Don't miss the view of Paris through the giant clock face.",
                    "crowd_level": "High"
                }
            ],
            "transportation": {
                "options": [
                    {
                        "type": "Metro",
                        "cost": "€1.90 per ticket, €14.90 for 10 tickets",
                        "hours": "5:30 AM - 1:15 AM (2:15 AM on weekends)",
                        "coverage": "Excellent throughout the city",
                        "ease_of_use": "Very easy with clear maps and frequent service"
                    },
                    {
                        "type": "Bus",
                        "cost": "€1.90 per ticket, same as Metro",
                        "hours": "5:30 AM - 12:30 AM",
                        "coverage": "Comprehensive, reaches areas not covered by Metro",
                        "ease_of_use": "Moderate, requires more knowledge of routes"
                    },
                    {
                        "type": "RER (Regional Express)",
                        "cost": "€1.90 - €12.10 depending on zones",
                        "hours": "5:00 AM - 1:00 AM",
                        "coverage": "Connects city center with suburbs and airports",
                        "ease_of_use": "Moderate, less frequent than Metro"
                    },
                    {
                        "type": "Taxi",
                        "cost": "€1.12 per km plus €2.60 base fare",
                        "hours": "24/7",
                        "coverage": "Complete",
                        "ease_of_use": "Easy but expensive"
                    },
                    {
                        "type": "Vélib' (Bike Sharing)",
                        "cost": "€3 for 24-hour pass, €20 for 7-day pass",
                        "hours": "24/7",
                        "coverage": "Good in central areas",
                        "ease_of_use": "Easy with smartphone app"
                    }
                ],
                "recommendation": "The Paris Metro is the most efficient way to get around the city. Consider purchasing a Paris Visite pass for unlimited travel.",
                "travel_passes": [
                    {
                        "name": "Paris Visite",
                        "duration": "1, 2, 3, or 5 days",
                        "coverage": "Unlimited travel on Metro, RER, bus, and tram",
                        "cost": "€13.20 - €72.40 depending on zones and duration"
                    },
                    {
                        "name": "Navigo Easy",
                        "duration": "Pay as you go",
                        "coverage": "Reloadable card for Metro, RER, bus, and tram",
                        "cost": "€2 for the card plus fare costs"
                    }
                ]
            },
            "cuisine": {
                "local_dishes": [
                    {
                        "name": "Coq au Vin",
                        "description": "Chicken braised with wine, lardons, mushrooms, and garlic",
                        "where_to_try": "Le Coq Rico, Au Petit Sud Ouest"
                    },
                    {
                        "name": "Boeuf Bourguignon",
                        "description": "Beef stew braised in red wine with carrots, onions, and mushrooms",
                        "where_to_try": "Allard, Le Petit Pontoise"
                    },
                    {
                        "name": "Croque Monsieur/Madame",
                        "description": "Grilled ham and cheese sandwich, topped with an egg for Madame",
                        "where_to_try": "Café de Flore, Les Deux Magots"
                    },
                    {
                        "name": "Escargots de Bourgogne",
                        "description": "Snails baked in their shells with garlic butter",
                        "where_to_try": "L'Escargot Montorgueil, Benoit"
                    },
                    {
                        "name": "Macarons",
                        "description": "Sweet meringue-based confection with ganache filling",
                        "where_to_try": "Ladurée, Pierre Hermé"
                    }
                ],
                "recommended_restaurants": [
                    {
                        "name": "Le Jules Verne",
                        "cuisine": "Modern French",
                        "price_range": "€€€€",
                        "rating": 4.5,
                        "address": "Eiffel Tower, 2nd floor",
                        "signature_dish": "Roasted Pigeon with Foie Gras",
                        "reservation": "Required, 2-3 months in advance"
                    },
                    {
                        "name": "Chez L'Ami Jean",
                        "cuisine": "Basque-influenced French",
                        "price_range": "€€€",
                        "rating": 4.7,
                        "address": "27 Rue Malar",
                        "signature_dish": "Rice Pudding",
                        "reservation": "Recommended"
                    },
                    {
                        "name": "Le Comptoir du Relais",
                        "cuisine": "Classic French Bistro",
                        "price_range": "€€",
                        "rating": 4.6,
                        "address": "9 Carrefour de l'Odéon",
                        "signature_dish": "Terrine de Campagne",
                        "reservation": "Dinner only, lunch is walk-in"
                    },
                    {
                        "name": "Breizh Café",
                        "cuisine": "Crêpes & Galettes",
                        "price_range": "€€",
                        "rating": 4.5,
                        "address": "109 Rue Vieille du Temple",
                        "signature_dish": "Complète Galette",
                        "reservation": "Recommended for weekends"
                    }
                ],
                "food_experiences": [
                    {
                        "name": "Paris Food Markets",
                        "description": "Visit local markets like Marché d'Aligre or Marché Bastille",
                        "cost": "Free to enter, pay for purchases"
                    },
                    {
                        "name": "Chocolate and Pastry Tours",
                        "description": "Guided tours of Paris's finest patisseries and chocolatiers",
                        "cost": "€70 - €120"
                    },
                    {
                        "name": "Wine Tasting",
                        "description": "Guided tastings of French wines in historic cellars",
                        "cost": "€30 - €150"
                    }
                ]
            },
            "travel_documents": {
                "visa_requirements": {
                    "EU_citizens": "No visa required",
                    "US_citizens": "No visa required for stays under 90 days",
                    "UK_citizens": "No visa required for stays under 90 days",
                    "other": "Check with French embassy or consulate"
                },
                "required_documents": [
                    "Valid passport (valid for at least 3 months beyond stay)",
                    "Return ticket",
                    "Proof of accommodation",
                    "Travel insurance (recommended)"
                ],
                "customs_regulations": "Standard EU regulations apply. Duty-free allowances include 200 cigarettes, 1L of spirits, 4L of wine."
            },
            "safety": {
                "overall_rating": "Generally safe",
                "areas_to_avoid": ["Northern suburbs at night", "Les Halles area late at night"],
                "common_scams": ["Petition scams", "Ring/gold scams", "Friendship bracelet scams"],
                "emergency_numbers": {
                    "general_emergency": "112",
                    "police": "17",
                    "ambulance": "15",
                    "fire": "18"
                },
                "safety_tips": [
                    "Be aware of pickpockets, especially in tourist areas and on public transport",
                    "Keep a copy of your passport separate from the original",
                    "Use hotel safes for valuables",
                    "Stay alert in crowded areas and train stations"
                ]
            }
        },
        "London": {
            "weather": {
                "spring": {
                    "description": "Mild with occasional showers and sunny spells",
                    "temperature": "8°C - 17°C",
                    "precipitation": "Moderate",
                    "best_activities": ["Park visits", "Museum hopping", "Walking tours"]
                },
                "summer": {
                    "description": "Warm with occasional hot days and mild evenings",
                    "temperature": "15°C - 25°C",
                    "precipitation": "Low to moderate",
                    "best_activities": ["Outdoor festivals", "Thames cruises", "Outdoor dining"]
                },
                "fall": {
                    "description": "Cool and often rainy with beautiful autumn colors",
                    "temperature": "8°C - 15°C",
                    "precipitation": "High",
                    "best_activities": ["Theater shows", "Museum visits", "Cozy pubs"]
                },
                "winter": {
                    "description": "Cold with occasional frost and rare snow",
                    "temperature": "2°C - 10°C",
                    "precipitation": "Moderate",
                    "best_activities": ["Christmas markets", "Indoor attractions", "Winter sales shopping"]
                }
            },
            "attractions": [
                {
                    "name": "British Museum",
                    "description": "World-famous museum of art and antiquities from around the world",
                    "rating": 4.8,
                    "price": "Free (donations encouraged)",
                    "hours": "10:00 AM - 5:00 PM, Friday until 8:30 PM",
                    "address": "Great Russell St, Bloomsbury",
                    "tips": "Visit early or late in the day to avoid crowds. Don't miss the Rosetta Stone and Egyptian mummies.",
                    "crowd_level": "High"
                },
                {
                    "name": "Tower of London",
                    "description": "Historic castle and former royal residence housing the Crown Jewels",
                    "rating": 4.7,
                    "price": "£29.90 for adults",
                    "hours": "9:00 AM - 4:30 PM (summer hours longer)",
                    "address": "Tower Hill",
                    "tips": "Join a Yeoman Warder tour for fascinating stories. See the Crown Jewels early to avoid long queues.",
                    "crowd_level": "Very High"
                },
                {
                    "name": "Buckingham Palace",
                    "description": "The Queen's official London residence with Changing of the Guard ceremony",
                    "rating": 4.6,
                    "price": "£30 for State Rooms (summer only), Changing of the Guard is free",
                    "hours": "State Rooms open July-September, Changing of the Guard at 11:00 AM",
                    "address": "Westminster",
                    "tips": "Arrive early (10:15 AM) for good viewing spots for the Changing of the Guard.",
                    "crowd_level": "Very High"
                },
                {
                    "name": "The Shard",
                    "description": "Tallest building in the UK with panoramic viewing gallery",
                    "rating": 4.5,
                    "price": "£32 for adults",
                    "hours": "10:00 AM - 10:00 PM",
                    "address": "32 London Bridge St",
                    "tips": "Book tickets in advance for sunset views. Consider having a drink at one of the bars instead of paying for the viewing platform.",
                    "crowd_level": "Moderate"
                },
                {
                    "name": "Tate Modern",
                    "description": "Modern art gallery housed in former power station",
                    "rating": 4.5,
                    "price": "Free (special exhibitions have fees)",
                    "hours": "10:00 AM - 6:00 PM, Friday and Saturday until 10:00 PM",
                    "address": "Bankside",
                    "tips": "Visit the free viewing terrace for great views of St. Paul's Cathedral and the Thames.",
                    "crowd_level": "High"
                }
            ]
        }
    }
    
    # Generic information for destinations not in our database
    generic_info = {
        "weather": {
            "spring": {
                "description": "Mild and pleasant with occasional showers",
                "temperature": "15°C - 22°C",
                "precipitation": "Moderate",
                "best_activities": ["Sightseeing", "Outdoor cafés", "Walking tours"]
            },
            "summer": {
                "description": "Warm and sunny with occasional hot days",
                "temperature": "22°C - 30°C",
                "precipitation": "Low",
                "best_activities": ["Beach visits", "Outdoor festivals", "Evening dining"]
            },
            "fall": {
                "description": "Cool and crisp with beautiful foliage",
                "temperature": "12°C - 20°C",
                "precipitation": "Moderate",
                "best_activities": ["Museum visits", "Food tours", "Photography walks"]
            },
            "winter": {
                "description": "Cold with occasional precipitation",
                "temperature": "5°C - 12°C",
                "precipitation": "Moderate",
                "best_activities": ["Indoor attractions", "Local cuisine", "Shopping"]
            }
        },
        "attractions": [
            {
                "name": f"{destination} Museum of Art",
                "description": "A world-class art museum featuring local and international exhibits.",
                "rating": 4.7,
                "price": "$20",
                "hours": "10:00 AM - 6:00 PM, Closed Mondays",
                "address": "123 Museum Avenue",
                "tips": "Visit on weekday mornings for smaller crowds.",
                "crowd_level": "Moderate"
            },
            {
                "name": f"{destination} Historical District",
                "description": "Explore the rich history and architecture of the city.",
                "rating": 4.5,
                "price": "Free",
                "hours": "Always open",
                "address": "Old Town",
                "tips": "Join a walking tour to learn about the local history.",
                "crowd_level": "Low"
            },
            {
                "name": f"{destination} Botanical Gardens",
                "description": "Beautiful gardens featuring local and exotic plants.",
                "rating": 4.6,
                "price": "$15",
                "hours": "9:00 AM - 5:00 PM",
                "address": "456 Garden Road",
                "tips": "Spring and early summer offer the best blooms.",
                "crowd_level": "Low"
            }
        ],
        "transportation": {
            "options": [
                {
                    "type": "Public Transit",
                    "cost": "$2-5 per ride",
                    "hours": "6:00 AM - 12:00 AM",
                    "coverage": "Good in central areas",
                    "ease_of_use": "Moderate"
                },
                {
                    "type": "Taxi",
                    "cost": "$10-20 for short trips",
                    "hours": "24/7",
                    "coverage": "Complete",
                    "ease_of_use": "Easy but expensive"
                },
                {
                    "type": "Rental Car",
                    "cost": "$40-80 per day",
                    "hours": "Agency hours vary",
                    "coverage": "Complete",
                    "ease_of_use": "Requires navigation skills"
                },
                {
                    "type": "Walking",
                    "cost": "Free",
                    "hours": "24/7",
                    "coverage": "Limited to central areas",
                    "ease_of_use": "Easy and healthy"
                }
            ],
            "recommendation": f"Walking is the best way to explore central {destination}, with public transit or taxis for longer distances."
        },
        "cuisine": {
            "local_dishes": [
                {
                    "name": f"{destination} Specialty Dish",
                    "description": "A local favorite made with regional ingredients",
                    "where_to_try": "Local Restaurant, Traditional Eatery"
                },
                {
                    "name": "Regional Delicacy",
                    "description": "Unique dish with historical significance",
                    "where_to_try": "Old Town Restaurant, Market Square Café"
                },
                {
                    "name": "Traditional Dessert",
                    "description": "Sweet treat made using traditional methods",
                    "where_to_try": "Historic Bakery, Sweet Shop"
                }
            ],
            "recommended_restaurants": [
                {
                    "name": f"The {destination} Grill",
                    "cuisine": "Local",
                    "price_range": "$$$",
                    "rating": 4.6,
                    "address": "123 Main Street",
                    "signature_dish": "Grilled Local Specialty",
                    "reservation": "Recommended"
                },
                {
                    "name": "Riverside Restaurant",
                    "cuisine": "International",
                    "price_range": "$$",
                    "rating": 4.4,
                    "address": "45 Waterfront Drive",
                    "signature_dish": "Seafood Platter",
                    "reservation": "Weekends only"
                }
            ]
        },
        "travel_documents": {
            "visa_requirements": {
                "general": "Varies by nationality, check with local embassy"
            },
            "required_documents": [
                "Valid passport",
                "Return ticket",
                "Proof of accommodation",
                "Travel insurance (recommended)"
            ],
            "customs_regulations": "Standard regulations apply. Check for restrictions on food, plants, and animals."
        },
        "safety": {
            "overall_rating": "Generally safe for tourists",
            "areas_to_avoid": ["Outskirts at night", "Isolated areas"],
            "common_scams": ["Tourist overcharging", "Pickpocketing in crowded areas"],
            "emergency_numbers": {
                "general_emergency": "Check local information",
                "police": "Check local information",
                "ambulance": "Check local information"
            },
            "safety_tips": [
                "Keep valuables secure and out of sight",
                "Be aware of your surroundings in crowded areas",
                "Use reputable transportation services",
                "Keep copies of important documents"
            ]
        }
    }
    
    # Get destination-specific info or use generic
    info = destination_info.get(destination, generic_info)
    
    # Filter based on topic if specified
    if topic.lower() in ["weather", "climate"]:
        return {"weather": info["weather"]}
    elif topic.lower() in ["attractions", "sights", "sightseeing", "things to do"]:
        return {"attractions": info["attractions"]}
    elif topic.lower() in ["transportation", "getting around", "transit"]:
        return {"transportation": info["transportation"]}
    elif topic.lower() in ["food", "cuisine", "restaurants", "dining"]:
        return {"cuisine": info["cuisine"]}
    elif topic.lower() in ["visa", "documents", "travel documents", "entry requirements"]:
        return {"travel_documents": info.get("travel_documents", generic_info["travel_documents"])}
    elif topic.lower() in ["safety", "security", "emergency"]:
        return {"safety": info.get("safety", generic_info["safety"])}
    else:
        # Return all information if topic is not specific
        return info
