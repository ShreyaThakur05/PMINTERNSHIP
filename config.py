import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Atlas Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://username:password@cluster.mongodb.net/internship_system')
    
    # Quota Configuration
    QUOTA_CONFIG = {
        'SC': 0.15,  # 15%
        'ST': 0.075, # 7.5%
        'OBC': 0.27, # 27%
        'ASPIRATIONAL_DISTRICTS': 0.20 # 20%
    }
    
    # Simple scoring weights
    SCORING_WEIGHTS = {
        'skill_match': 0.4,
        'location_match': 0.2,
        'sector_match': 0.2,
        'cgpa': 0.2
    }
    
    # API Configuration
    API_HOST = '0.0.0.0'
    API_PORT = 5000
    DEBUG = True