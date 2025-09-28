import pandas as pd
from faker import Faker
import random
import json

# Initialize Faker to generate Indian-style data for realism
fake = Faker('en_IN')

# --- Configuration: Define the universe of possible data ---
# This dictionary links majors to a realistic set of skills.
MAJORS_SKILLS = {
    "Computer Science": ["Python", "Java", "C++", "SQL", "React", "Node.js", "Cloud Computing", "Docker"],
    "Mechanical Engineering": ["AutoCAD", "SolidWorks", "MATLAB", "3D Printing", "Thermodynamics", "FEA"],
    "Finance": ["Financial Modeling", "Excel", "Tally", "Statistics", "Risk Analysis", "QuickBooks"],
    "Marketing": ["SEO", "Google Analytics", "Social Media Marketing", "Content Creation", "Email Marketing"]
}

# Define common locations, sectors, and universities for randomization
LOCATIONS = ["Pune", "Mumbai", "Bangalore", "Delhi", "Hyderabad", "Chennai"]
SECTORS = ["IT", "Finance", "Manufacturing", "Marketing", "Healthcare"]
UNIVERSITIES = ["Pune University", "Mumbai University", "Delhi University", "VIT", "MIT"]

# --- Generate Student Data ---
students_data = []
for i in range(1000):
    # Randomly select a major for each student
    major = random.choice(list(MAJORS_SKILLS.keys()))
    
    # **Robust Fix**: Dynamically determine how many skills to pick.
    # It will pick a number between 3 and the total number of skills available for that major.
    available_skills = MAJORS_SKILLS[major]
    max_skills_for_major = len(available_skills)
    num_skills = random.randint(3, max_skills_for_major)
    
    # Safely sample the skills
    skills = random.sample(available_skills, num_skills)
    
    # Append the generated student record to our list
    students_data.append({
        "StudentID": 1000 + i,
        "FirstName": fake.first_name(),
        "LastName": fake.last_name(),
        "University": random.choice(UNIVERSITIES),
        "Major": major,
        "CGPA": round(random.uniform(6.5, 9.8), 2),
        "Skills": ",".join(skills),
        "LocationPreferences": ",".join(random.sample(LOCATIONS, 2)),
        "SectorInterests": ",".join(random.sample(SECTORS, 2)),
        "IsFromRuralArea": random.choices([True, False], weights=[0.20, 0.80])[0],
        "IsFromAspirational": random.choices([True, False], weights=[0.15, 0.85])[0],
        "SocialCategory": random.choice(["GEN", "OBC", "SC", "ST"]),
        "Gender": random.choice(["Male", "Female"]),
        "PastParticipation": random.choices([True, False], weights=[0.05, 0.95])[0],
        "ProjectDescription": fake.paragraph(nb_sentences=3)
    })

# Convert the list of dictionaries to a pandas DataFrame and save to CSV
students_df = pd.DataFrame(students_data)
students_df.to_csv('students.csv', index=False)
print("Generated students.csv with 1000 records successfully!")

# --- Generate Internship Data ---
internships_data = []
for i in range(100):
    # Randomly select a sector for the internship
    sector = random.choice(SECTORS)
    
    # Infer a related major to generate realistic skill requirements
    related_major = "Computer Science"  # Default
    if sector == "Finance": related_major = "Finance"
    if sector == "Marketing": related_major = "Marketing"
    if sector == "Manufacturing": related_major = "Mechanical Engineering"
    
    # Safely determine the number of required skills based on the related major
    available_skills = MAJORS_SKILLS[related_major]
    max_skills_for_major = len(available_skills)
    num_skills = random.randint(2, max_skills_for_major)
    skills = random.sample(available_skills, num_skills)

    # Append the generated internship record to our list
    internships_data.append({
        "InternshipID": 500 + i,
        "CompanyName": fake.company(),
        "CompanyTier": random.randint(1, 3),
        "RoleTitle": f"{sector} Intern",
        "Sector": sector,
        "Location": random.choice(LOCATIONS),
        "RequiredSkills": ",".join(skills),
        "RoleDescription": fake.paragraph(nb_sentences=5),
        "Capacity": random.randint(1, 10)
    })

# Convert the list of dictionaries to a pandas DataFrame and save to CSV
internships_df = pd.DataFrame(internships_data)
internships_df.to_csv('internships.csv', index=False)
print("Generated internships.csv with 100 records successfully!")