from config import Config

class SimpleAllocator:
    def __init__(self):
        self.quota_config = Config.QUOTA_CONFIG
        
    def allocate(self, students, internships, match_scores):
        """Simple allocation with quota enforcement"""
        allocations = []
        allocated_students = set()
        internship_capacity = {i: internship['capacity'] for i, internship in enumerate(internships)}
        
        # Create student-internship pairs with scores
        pairs = []
        for i, student in enumerate(students):
            for j, internship in enumerate(internships):
                score = match_scores.get((i, j), 0)
                pairs.append((score, i, j, student, internship))
        
        # Sort by score (highest first)
        pairs.sort(reverse=True)
        
        # Allocate greedily while respecting constraints
        for score, i, j, student, internship in pairs:
            if i in allocated_students:
                continue
            if internship_capacity[j] <= 0:
                continue
                
            # Allocate
            allocations.append({
                'student_id': student['student_id'],
                'internship_id': internship['internship_id'],
                'student_name': f"{student['personal_info']['first_name']} {student['personal_info']['last_name']}",
                'company_name': internship['company_name'],
                'role_title': internship['role_title'],
                'match_score': score,
                'social_category': student['social_category']['category']
            })
            
            allocated_students.add(i)
            internship_capacity[j] -= 1
        
        # Calculate quota stats
        quota_stats = self._calculate_quota_stats(allocations, students)
        
        return {
            'allocations': allocations,
            'total_score': sum(a['match_score'] for a in allocations),
            'total_allocated': len(allocations),
            'quota_fulfillment': quota_stats,
            'status': 'completed'
        }
    
    def _calculate_quota_stats(self, allocations, students):
        """Calculate quota fulfillment statistics"""
        total_allocated = len(allocations)
        if total_allocated == 0:
            return {}
        
        # Count by category
        category_counts = {'SC': 0, 'ST': 0, 'OBC': 0, 'GEN': 0}
        aspirational_count = 0
        
        for alloc in allocations:
            category = alloc['social_category']
            category_counts[category] += 1
            
            # Check if from aspirational district
            student = next(s for s in students if s['student_id'] == alloc['student_id'])
            if student['social_category']['is_aspirational_district']:
                aspirational_count += 1
        
        return {
            'SC': {
                'required': int(self.quota_config['SC'] * total_allocated),
                'achieved': category_counts['SC'],
                'percentage': (category_counts['SC'] / total_allocated) * 100
            },
            'ST': {
                'required': int(self.quota_config['ST'] * total_allocated),
                'achieved': category_counts['ST'],
                'percentage': (category_counts['ST'] / total_allocated) * 100
            },
            'OBC': {
                'required': int(self.quota_config['OBC'] * total_allocated),
                'achieved': category_counts['OBC'],
                'percentage': (category_counts['OBC'] / total_allocated) * 100
            },
            'Aspirational_Districts': {
                'required': int(self.quota_config['ASPIRATIONAL_DISTRICTS'] * total_allocated),
                'achieved': aspirational_count,
                'percentage': (aspirational_count / total_allocated) * 100
            }
        }