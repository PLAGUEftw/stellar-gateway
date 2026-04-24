"""
Database Seeder Script
Run this once to populate initial data in MongoDB
Usage: python seed_database.py
"""

from database import PlanetManager, MissionManager, Database
from datetime import datetime

PLANETS_DATA = [
    {
        'name': 'Mercury',
        'emoji': '☿',
        'description': 'The smallest planet and closest to the Sun, with extreme temperature variations.',
        'diameter': '4,879 km',
        'distance': '57.9 million km',
        'moons': 0,
        'day_length': '59 Earth days',
        'year_length': '88 Earth days',
        'temperature': '-173°C to 427°C',
        'gravity': '3.7 m/s²',
        'color': '#8c7853',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Mercury_in_true_color.jpg',
        'facts': [
            'Mercury has no atmosphere',
            'A year on Mercury is just 88 Earth days',
            'It has the most craters in our solar system'
        ],
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Venus',
        'emoji': '♀',
        'description': 'The hottest planet with a thick, toxic atmosphere of carbon dioxide.',
        'diameter': '12,104 km',
        'distance': '108.2 million km',
        'moons': 0,
        'day_length': '243 Earth days',
        'year_length': '225 Earth days',
        'temperature': '462°C',
        'gravity': '8.87 m/s²',
        'color': '#e8b06c',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/e/e5/Venus-real_color.jpg',
        'facts': [
            'Venus rotates backwards compared to other planets',
            'It\'s the hottest planet despite not being closest to the Sun',
            'A day on Venus is longer than its year'
        ],
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Earth',
        'emoji': '🌍',
        'description': 'Our home planet, the only known world with life in the universe.',
        'diameter': '12,742 km',
        'distance': '149.6 million km',
        'moons': 1,
        'day_length': '24 hours',
        'year_length': '365.25 days',
        'temperature': '-88°C to 58°C',
        'gravity': '9.8 m/s²',
        'color': '#4a90e2',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg',
        'facts': [
            'Earth is 4.54 billion years old',
            '71% of Earth\'s surface is water',
            'Earth has a powerful magnetic field'
        ],
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Mars',
        'emoji': '♂',
        'description': 'The Red Planet, a potential future home for human colonization.',
        'diameter': '6,779 km',
        'distance': '227.9 million km',
        'moons': 2,
        'day_length': '24.6 hours',
        'year_length': '687 Earth days',
        'temperature': '-87°C to -5°C',
        'gravity': '3.71 m/s²',
        'color': '#cd5c5c',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/0/02/OSIRIS_Mars_true_color.jpg',
        'facts': [
            'Mars has the largest volcano - Olympus Mons',
            'A day on Mars is similar to Earth',
            'Mars has two moons: Phobos and Deimos'
        ],
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Jupiter',
        'emoji': '♃',
        'description': 'The largest planet with a Great Red Spot storm bigger than Earth.',
        'diameter': '139,820 km',
        'distance': '778.5 million km',
        'moons': 95,
        'day_length': '9.9 hours',
        'year_length': '11.86 Earth years',
        'temperature': '-108°C',
        'gravity': '24.79 m/s²',
        'color': '#daa520',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/e/e2/Jupiter.jpg',
        'facts': [
            'Jupiter has the shortest day of all planets',
            'The Great Red Spot is a storm lasting 350+ years',
            'Jupiter has at least 95 moons'
        ],
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Saturn',
        'emoji': '♄',
        'description': 'Famous for its stunning ring system made of ice and rock.',
        'diameter': '116,460 km',
        'distance': '1.43 billion km',
        'moons': 146,
        'day_length': '10.7 hours',
        'year_length': '29.46 Earth years',
        'temperature': '-138°C',
        'gravity': '10.44 m/s²',
        'color': '#f4c430',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Saturn_during_Equinox.jpg',
        'facts': [
            'Saturn has 146 known moons',
            'Saturn could float on water (if you could find a big enough pool!)',
            'Its rings are made of ice and rock particles'
        ],
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Uranus',
        'emoji': '♅',
        'description': 'An ice giant that rotates on its side, with a bluish-green color.',
        'diameter': '50,724 km',
        'distance': '2.87 billion km',
        'moons': 27,
        'day_length': '17.2 hours',
        'year_length': '84 Earth years',
        'temperature': '-195°C',
        'gravity': '8.69 m/s²',
        'color': '#4fd0e0',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/3/3d/Uranus2.jpg',
        'facts': [
            'Uranus rotates on its side at 98 degrees',
            'It was the first planet discovered with a telescope',
            'Uranus has 13 faint rings'
        ],
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Neptune',
        'emoji': '♆',
        'description': 'The windiest planet with supersonic winds reaching 2,100 km/h.',
        'diameter': '49,244 km',
        'distance': '4.5 billion km',
        'moons': 14,
        'day_length': '16.1 hours',
        'year_length': '165 Earth years',
        'temperature': '-201°C',
        'gravity': '11.15 m/s²',
        'color': '#4166f5',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/5/56/Neptune_Full.jpg',
        'facts': [
            'Neptune has the strongest winds in the solar system',
            'It takes 165 Earth years to orbit the Sun',
            'Neptune was discovered through mathematical predictions'
        ],
        'created_at': datetime.utcnow()
    }
]

MISSIONS_DATA = [
    {
        'name': 'Apollo 11',
        'year': 1969,
        'agency': 'NASA',
        'description': 'First human mission to land on the Moon. Neil Armstrong and Buzz Aldrin walked on the lunar surface.',
        'status': 'Completed',
        'icon': '🚀',
        'duration': '8 days',
        'crew': ['Neil Armstrong', 'Buzz Aldrin', 'Michael Collins'],
        'destination': 'Moon',
        'cost': '$355 million',
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Voyager 1',
        'year': 1977,
        'agency': 'NASA',
        'description': 'Launched to study outer planets. Now in interstellar space, the farthest human-made object.',
        'status': 'Active',
        'icon': '🛰️',
        'duration': 'Ongoing (47+ years)',
        'crew': ['Unmanned'],
        'destination': 'Interstellar Space',
        'cost': '$865 million',
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Hubble Space Telescope',
        'year': 1990,
        'agency': 'NASA/ESA',
        'description': 'Revolutionary space telescope that has captured stunning images of the universe for over 30 years.',
        'status': 'Active',
        'icon': '🔭',
        'duration': 'Ongoing (34+ years)',
        'crew': ['Unmanned'],
        'destination': 'Low Earth Orbit',
        'cost': '$16 billion',
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Mars Curiosity Rover',
        'year': 2012,
        'agency': 'NASA',
        'description': 'Exploring Mars to assess whether the planet ever had conditions suitable for microbial life.',
        'status': 'Active',
        'icon': '🤖',
        'duration': 'Ongoing (12+ years)',
        'crew': ['Unmanned'],
        'destination': 'Mars',
        'cost': '$2.5 billion',
        'created_at': datetime.utcnow()
    },
    {
        'name': 'James Webb Space Telescope',
        'year': 2021,
        'agency': 'NASA/ESA/CSA',
        'description': 'The most powerful space telescope ever built, observing the universe in infrared light.',
        'status': 'Active',
        'icon': '🌟',
        'duration': 'Ongoing',
        'crew': ['Unmanned'],
        'destination': 'L2 Lagrange Point',
        'cost': '$10 billion',
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Chandrayaan-3',
        'year': 2023,
        'agency': 'ISRO',
        'description': 'India\'s successful lunar mission that made a soft landing near the Moon\'s south pole.',
        'status': 'Completed',
        'icon': '🌙',
        'duration': '40 days',
        'crew': ['Unmanned'],
        'destination': 'Moon South Pole',
        'cost': '$75 million',
        'created_at': datetime.utcnow()
    },
    {
        'name': 'Artemis Program',
        'year': 2024,
        'agency': 'NASA',
        'description': 'Program to return humans to the Moon and establish sustainable exploration by 2025.',
        'status': 'Upcoming',
        'icon': '👨‍🚀',
        'duration': 'Ongoing Program',
        'crew': ['To be announced'],
        'destination': 'Moon',
        'cost': '$93 billion',
        'created_at': datetime.utcnow()
    },
    {
        'name': 'SpaceX Starship',
        'year': 2024,
        'agency': 'SpaceX',
        'description': 'Fully reusable spacecraft designed for missions to Mars and beyond.',
        'status': 'Testing',
        'icon': '🛸',
        'duration': 'Ongoing Development',
        'crew': ['To be announced'],
        'destination': 'Mars (Planned)',
        'cost': '$5 billion+',
        'created_at': datetime.utcnow()
    }
]


def seed_database():
    """Seed the database with initial data"""
    print("\n" + "="*50)
    print("🌱 STELLAR GATEWAY DATABASE SEEDER")
    print("="*50 + "\n")
    
    db = Database()
    if not db.is_connected():
        print("❌ Database connection failed! Cannot seed data.")
        return
    
    # Seed Planets
    print("🪐 Seeding Planets...")
    planet_manager = PlanetManager()
    planet_count = 0
    for planet in PLANETS_DATA:
        if planet_manager.add_planet(planet):
            planet_count += 1
            print(f"   ✅ Added: {planet['name']}")
        else:
            print(f"   ⚠️  Skipped: {planet['name']} (already exists)")
    print(f"\n   Total planets added: {planet_count}/{len(PLANETS_DATA)}\n")
    
    # Seed Missions
    print("🚀 Seeding Missions...")
    mission_manager = MissionManager()
    mission_count = 0
    for mission in MISSIONS_DATA:
        if mission_manager.add_mission(mission):
            mission_count += 1
            print(f"   ✅ Added: {mission['name']}")
    print(f"\n   Total missions added: {mission_count}/{len(MISSIONS_DATA)}\n")
    
    print("="*50)
    print("✨ Database seeding completed successfully!")
    print("="*50 + "\n")


def clear_database():
    """Clear all data from database (use with caution!)"""
    print("\n⚠️  WARNING: This will delete all data!")
    confirm = input("Type 'YES' to confirm: ")
    
    if confirm != 'YES':
        print("❌ Operation cancelled")
        return
    
    db = Database()
    if not db.is_connected():
        print("❌ Database connection failed!")
        return
    
    database = db.get_db()
    collections = ['users', 'activities', 'favorites', 'planets', 'missions']
    
    for coll_name in collections:
        result = database[coll_name].delete_many({})
        print(f"🗑️  Cleared {coll_name}: {result.deleted_count} documents")
    
    print("\n✅ Database cleared successfully!")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--clear':
        clear_database()
    else:
        seed_database()