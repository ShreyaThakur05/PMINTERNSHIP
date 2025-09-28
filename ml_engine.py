import numpy as np
import pandas as pd
from config import Config

class MatchingEngine:
    def __init__(self):
        self.xgb_model = None
        
    def generate_embeddings(self, text_list):
        """Generate simple embeddings for text data"""
        # Simple word count based embedding
        return [len(text.split()) for text in text_list]
    
    def calculate_skill_match(self, student_skills, required_skills):
        """Calculate skill match percentage"""
        student_set = set([s.strip().lower() for s in student_skills])
        required_set = set([s.strip().lower() for s in required_skills])
        
        if not required_set:
            return 0.0
        
        intersection = student_set.intersection(required_set)
        return len(intersection) / len(required_set)
    
    def extract_features(self, student, internship):
        """Extract features for ML model"""
        features = {}
        
        # Skill matching
        features['skill_match'] = self.calculate_skill_match(
            student['skills'], internship['required_skills']
        )
        
        # Location preference
        features['location_match'] = int(
            internship['location'] in student['preferences']['locations']
        )
        
        # Sector preference
        features['sector_match'] = int(
            internship['sector'] in student['preferences']['sectors']
        )
        
        # Academic performance
        features['cgpa_normalized'] = student['personal_info']['cgpa'] / 10.0
        
        # Social category features
        features['is_sc'] = int(student['social_category']['category'] == 'SC')
        features['is_st'] = int(student['social_category']['category'] == 'ST')
        features['is_obc'] = int(student['social_category']['category'] == 'OBC')
        features['is_rural'] = int(student['social_category']['is_rural'])
        features['is_aspirational'] = int(student['social_category']['is_aspirational_district'])
        
        # Past participation
        features['past_participation'] = int(student['past_participation'])
        
        # Company tier
        features['company_tier'] = internship['company_tier']
        
        return features
    
    def calculate_match_score(self, student, internship):
        """Calculate match score between student and internship"""
        features = self.extract_features(student, internship)
        
        # Simple weighted scoring if no ML model
        if self.xgb_model is None:
            score = (
                features['skill_match'] * 0.4 +
                features['location_match'] * 0.2 +
                features['sector_match'] * 0.2 +
                features['cgpa_normalized'] * 0.2
            )
            return min(score, 1.0)
        
        # Use simple scoring since no ML model
        return min(score, 1.0)
    
    def train_model(self, training_data):
        """Simple model training placeholder"""
        if not training_data:
            return
        print("Model training completed (simplified version)")