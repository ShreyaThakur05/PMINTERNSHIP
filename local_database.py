import pandas as pd
import json
import os

class LocalDatabaseManager:
    def __init__(self):
        self.students_file = 'students_db.json'
        self.internships_file = 'internships_db.json'
        self.allocations_file = 'allocations_db.json'
        
    def load_students_from_csv(self, csv_path='students.csv'):
        """Load students data from CSV to local JSON"""
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
        
        with open(self.students_file, 'w') as f:
            json.dump(students, f, indent=2)
        
        return len(students)
    
    def load_internships_from_csv(self, csv_path='internships.csv'):
        """Load internships data from CSV to local JSON"""
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
        
        with open(self.internships_file, 'w') as f:
            json.dump(internships, f, indent=2)
        
        return len(internships)
    
    def get_students(self):
        if os.path.exists(self.students_file):
            with open(self.students_file, 'r') as f:
                return json.load(f)
        return []
    
    def get_internships(self):
        if os.path.exists(self.internships_file):
            with open(self.internships_file, 'r') as f:
                return json.load(f)
        return []
    
    def get_allocations(self):
        if os.path.exists(self.allocations_file):
            with open(self.allocations_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_allocation(self, allocation_data):
        allocations = []
        if os.path.exists(self.allocations_file):
            with open(self.allocations_file, 'r') as f:
                allocations = json.load(f)
        
        allocations.append(allocation_data)
        
        with open(self.allocations_file, 'w') as f:
            json.dump(allocations, f, indent=2)
        
        return True