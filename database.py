from pymongo import MongoClient
from config import Config
import pandas as pd

class DatabaseManager:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client.internship_system
        
    def load_students_from_csv(self, csv_path='students.csv'):
        """Load students data from CSV to MongoDB"""
        df = pd.read_csv(csv_path)
        students = []
        
        for _, row in df.iterrows():
            student = {
                'student_id': str(row['StudentID']),
                'personal_info': {
                    'first_name': row['FirstName'],
                    'last_name': row['LastName'],
                    'university': row['University'],
                    'major': row['Major'],
                    'cgpa': row['CGPA'],
                    'gender': row['Gender']
                },
                'skills': row['Skills'].split(','),
                'preferences': {
                    'locations': row['LocationPreferences'].split(','),
                    'sectors': row['SectorInterests'].split(',')
                },
                'social_category': {
                    'category': row['SocialCategory'],
                    'is_rural': row['IsFromRuralArea'],
                    'is_aspirational_district': row['IsFromAspirational']
                },
                'past_participation': row['PastParticipation'],
                'project_description': row['ProjectDescription']
            }
            students.append(student)
        
        self.db.students.delete_many({})
        self.db.students.insert_many(students)
        return len(students)
    
    def load_internships_from_csv(self, csv_path='internships.csv'):
        """Load internships data from CSV to MongoDB"""
        df = pd.read_csv(csv_path)
        internships = []
        
        for _, row in df.iterrows():
            internship = {
                'internship_id': str(row['InternshipID']),
                'company_name': row['CompanyName'],
                'company_tier': row['CompanyTier'],
                'role_title': row['RoleTitle'],
                'sector': row['Sector'],
                'location': row['Location'],
                'required_skills': row['RequiredSkills'].split(','),
                'role_description': row['RoleDescription'],
                'capacity': row['Capacity']
            }
            internships.append(internship)
        
        self.db.internships.delete_many({})
        self.db.internships.insert_many(internships)
        return len(internships)
    
    def get_students(self):
        return list(self.db.students.find())
    
    def get_internships(self):
        return list(self.db.internships.find())
    
    def save_allocation(self, allocation_data):
        return self.db.allocations.insert_one(allocation_data)