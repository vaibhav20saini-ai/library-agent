"""Sample library graph and book data for the Intelligent Library Agent."""

LIBRARY_GRAPH = {
    "Entrance": {"Reception": 2, "Main_Aisle": 4},
    "Reception": {"Entrance": 2, "Reference": 3, "Main_Aisle": 2},
    "Main_Aisle": {"Entrance": 4, "Reception": 2, "Aisle_A": 3, "Aisle_B": 4, "Computer_Section": 5},
    "Reference": {"Reception": 3, "Aisle_A": 2},
    "Aisle_A": {"Main_Aisle": 3, "Reference": 2, "Science_Shelf": 2, "History_Shelf": 4},
    "Aisle_B": {"Main_Aisle": 4, "Literature_Shelf": 2, "Restricted_Archive": 3},
    "Computer_Section": {"Main_Aisle": 5, "Technology_Shelf": 2},
    "Science_Shelf": {"Aisle_A": 2},
    "History_Shelf": {"Aisle_A": 4},
    "Literature_Shelf": {"Aisle_B": 2},
    "Technology_Shelf": {"Computer_Section": 2},
    "Restricted_Archive": {"Aisle_B": 3},
}

BOOKS = [
    {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "shelf": "Technology_Shelf", "available": True, "priority": 5},
    {"title": "Artificial Intelligence: A Modern Approach", "author": "Stuart Russell", "shelf": "Science_Shelf", "available": True, "priority": 5},
    {"title": "Python Crash Course", "author": "Eric Matthes", "shelf": "Technology_Shelf", "available": True, "priority": 4},
    {"title": "Database System Concepts", "author": "Abraham Silberschatz", "shelf": "Computer_Section", "available": True, "priority": 3},
    {"title": "Operating System Concepts", "author": "Abraham Silberschatz", "shelf": "Technology_Shelf", "available": False, "priority": 3},
    {"title": "A Brief History of Time", "author": "Stephen Hawking", "shelf": "History_Shelf", "available": True, "priority": 2},
    {"title": "The Alchemist", "author": "Paulo Coelho", "shelf": "Literature_Shelf", "available": True, "priority": 2},
    {"title": "Computer Networks", "author": "Andrew S. Tanenbaum", "shelf": "Computer_Section", "available": True, "priority": 4},
    {"title": "Encyclopedia of Rare Manuscripts", "author": "Library Archive", "shelf": "Restricted_Archive", "available": True, "priority": 1},
    {"title": "Fundamentals of Physics", "author": "Halliday, Resnick and Walker", "shelf": "Science_Shelf", "available": True, "priority": 3},
]


NODE_POSITIONS = {
    "Entrance": (0, 2), "Reception": (1, 3), "Main_Aisle": (2, 2),
    "Reference": (2, 4), "Aisle_A": (3, 3), "Aisle_B": (3, 1),
    "Computer_Section": (3, 2), "Science_Shelf": (4, 4),
    "History_Shelf": (4, 3), "Literature_Shelf": (4, 1),
    "Technology_Shelf": (4, 2), "Restricted_Archive": (4, 0),
}

CLOSED_SECTIONS_DEFAULT = []
RESTRICTED_SHELVES_DEFAULT = ["Restricted_Archive"]
CROWDED_AISLES_DEFAULT = ["Main_Aisle"]
