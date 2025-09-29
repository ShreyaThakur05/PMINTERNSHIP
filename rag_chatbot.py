import google.generativeai as genai
import json
import os
from datetime import datetime
from local_database import LocalDatabaseManager

class RAGChatbot:
    def __init__(self):
        genai.configure(api_key="AIzaSyBtcYwKghlA9nnvX7zsEyhS4Eki_1yc72s")
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.db = LocalDatabaseManager()
        
    def get_context_data(self):
        """Retrieve current system data for context"""
        try:
            students = self.db.get_students()
            internships = self.db.get_internships()
            allocations = self.db.get_allocations()
            
            print(f"Debug: Found {len(students)} students, {len(internships)} internships, {len(allocations)} allocations")
            
            # Create summary statistics
            total_students = len(students)
            total_internships = len(internships)
            allocated_count = len([a for a in allocations if a.get('allocated')])
            
            # Category breakdown
            categories = {}
            allocated_by_category = {}
            for student in students:
                cat = student.get('social_category', {}).get('category', 'General')
                categories[cat] = categories.get(cat, 0) + 1
            
            # Count allocated students by category
            for allocation in allocations:
                if allocation.get('allocated'):
                    cat = allocation.get('social_category', 'General')
                    allocated_by_category[cat] = allocated_by_category.get(cat, 0) + 1
            
            # Skills summary
            all_skills = []
            for student in students:
                all_skills.extend(student.get('skills', []))
            skill_counts = {}
            for skill in all_skills:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
            
            # Count IT internships
            it_internships = [i for i in internships if 'IT' in i.get('sector', '').upper() or 'Technology' in i.get('sector', '') or 'Software' in i.get('sector', '')]
            
            context = {
                "system_stats": {
                    "total_students": total_students,
                    "total_internships": total_internships,
                    "allocated_students": allocated_count,
                    "unallocated_students": total_students - allocated_count,
                    "it_internships": len(it_internships)
                },
                "category_distribution": categories,
                "allocated_by_category": allocated_by_category,
                "top_skills": dict(sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
                "quota_requirements": {
                    "SC": "15% (150 positions)",
                    "ST": "7.5% (75 positions)", 
                    "OBC": "27% (270 positions)",
                    "Aspirational Districts": "20% (200 positions)"
                },
                "definitions": {
                    "aspirational_districts": "Government-identified backward districts that need focused development. Students from these areas get 20% quota in internship allocation.",
                    "social_categories": {
                        "SC": "Scheduled Caste - 15% quota",
                        "ST": "Scheduled Tribe - 7.5% quota", 
                        "OBC": "Other Backward Classes - 27% quota",
                        "GEN": "General category"
                    }
                }
            }
            
            return context, students, internships, allocations
            
        except Exception as e:
            return {"error": str(e)}, [], [], []
    
    def query(self, user_question):
        """Process user query with RAG approach"""
        context_data, students, internships, allocations = self.get_context_data()
        
        # Create system prompt with current data context
        system_prompt = f"""
You are TrueNorth, an AI assistant for InternNet's Internship Allocation System. 

IMPORTANT RULES:
1. Answer ONLY based on the provided data below
2. If data shows 0 records, say "No data available yet. Please load data and run allocation first."
3. Stay focused on internship allocation topics only
4. Be precise with numbers from the data
5. Don't make assumptions or provide general information not in the data

CURRENT SYSTEM DATA:
{json.dumps(context_data, indent=2)}

ALLOCATION SYSTEM INFO:
- Government quotas: SC(15%), ST(7.5%), OBC(27%), Aspirational Districts(20%)
- Matching algorithm considers: skills(35%), CGPA(25%), location(15%), sector(10%), experience(10%), company_tier(5%)
- Each student gets maximum 1 internship

DATA AVAILABLE:
- {len(students)} students loaded
- {len(internships)} internships loaded  
- {len(allocations)} allocation records

Answer the user's question using only this data. Be helpful but stay within the data boundaries.
"""

        try:
            # Generate response using Gemini
            response = self.model.generate_content(
                f"{system_prompt}\n\nUser Question: {user_question}"
            )
            
            return {
                "answer": response.text,
                "timestamp": datetime.now().isoformat(),
                "context_used": True
            }
            
        except Exception as e:
            return {
                "answer": f"Error processing query: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "context_used": False
            }
    
    def get_detailed_data(self, query_type, filters=None):
        """Get specific data based on query type"""
        students = self.db.get_students()
        internships = self.db.get_internships()
        allocations = self.db.get_allocations()
        
        if query_type == "unallocated_students":
            allocated_ids = {a['student_id'] for a in allocations if a.get('allocated')}
            unallocated = [s for s in students if s['student_id'] not in allocated_ids]
            
            if filters:
                if 'skills' in filters:
                    unallocated = [s for s in unallocated 
                                 if any(skill.lower() in [sk.lower() for sk in s.get('skills', [])] 
                                       for skill in filters['skills'])]
                if 'category' in filters:
                    unallocated = [s for s in unallocated 
                                 if s.get('social_category') == filters['category']]
            
            return unallocated[:10]  # Limit results
            
        elif query_type == "allocation_by_company":
            company_allocations = {}
            for allocation in allocations:
                if allocation.get('allocated'):
                    company = allocation.get('company_name', 'Unknown')
                    if company not in company_allocations:
                        company_allocations[company] = []
                    company_allocations[company].append(allocation)
            return company_allocations
            
        return []