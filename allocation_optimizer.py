from config import Config
import random

class AllocationOptimizer:
    def __init__(self):
        self.quota_config = Config.QUOTA_CONFIG
        
    def optimize_allocation(self, students, internships, match_scores):
        """Optimize allocation using greedy algorithm with quota enforcement"""
        
        # Simple greedy allocation with quota enforcement
        allocations = []
        allocated_students = set()
        internship_capacity = {i: internship['capacity'] for i, internship in enumerate(internships)}
        
        # Decision variables: x[i,j] = 1 if student i assigned to internship j
        x = {}
        for i, student in enumerate(students):
            for j, internship in enumerate(internships):
                x[i, j] = pulp.LpVariable(f"x_{i}_{j}", cat='Binary')
        
        # Objective: Maximize total match scores
        prob += pulp.lpSum([
            match_scores.get((i, j), 0) * x[i, j]
            for i in range(len(students))
            for j in range(len(internships))
        ])
        
        # Constraint 1: Each student gets at most one internship
        for i in range(len(students)):
            prob += pulp.lpSum([x[i, j] for j in range(len(internships))]) <= 1
        
        # Constraint 2: Each internship capacity limit
        for j, internship in enumerate(internships):
            prob += pulp.lpSum([x[i, j] for i in range(len(students))]) <= internship['capacity']
        
        # Constraint 3: Quota requirements
        total_positions = sum(internship['capacity'] for internship in internships)
        
        # SC quota (15%)
        sc_students = [i for i, s in enumerate(students) 
                      if s['social_category']['category'] == 'SC']
        if sc_students:
            prob += pulp.lpSum([x[i, j] for i in sc_students 
                               for j in range(len(internships))]) >= int(self.quota_config['SC'] * total_positions)
        
        # ST quota (7.5%)
        st_students = [i for i, s in enumerate(students) 
                      if s['social_category']['category'] == 'ST']
        if st_students:
            prob += pulp.lpSum([x[i, j] for i in st_students 
                               for j in range(len(internships))]) >= int(self.quota_config['ST'] * total_positions)
        
        # OBC quota (27%)
        obc_students = [i for i, s in enumerate(students) 
                       if s['social_category']['category'] == 'OBC']
        if obc_students:
            prob += pulp.lpSum([x[i, j] for i in obc_students 
                               for j in range(len(internships))]) >= int(self.quota_config['OBC'] * total_positions)
        
        # Aspirational Districts quota (20%)
        aspirational_students = [i for i, s in enumerate(students) 
                               if s['social_category']['is_aspirational_district']]
        if aspirational_students:
            prob += pulp.lpSum([x[i, j] for i in aspirational_students 
                               for j in range(len(internships))]) >= int(self.quota_config['ASPIRATIONAL_DISTRICTS'] * total_positions)
        
        # Solve the problem
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        
        # Extract solution
        allocations = []
        total_score = 0
        
        for i, student in enumerate(students):
            for j, internship in enumerate(internships):
                if x[i, j].varValue == 1:
                    score = match_scores.get((i, j), 0)
                    allocations.append({
                        'student_id': student['student_id'],
                        'internship_id': internship['internship_id'],
                        'student_name': f"{student['personal_info']['first_name']} {student['personal_info']['last_name']}",
                        'company_name': internship['company_name'],
                        'role_title': internship['role_title'],
                        'match_score': score,
                        'social_category': student['social_category']['category']
                    })
                    total_score += score
        
        # Calculate quota fulfillment
        quota_stats = self._calculate_quota_stats(allocations, students)
        
        return {
            'allocations': allocations,
            'total_score': total_score,
            'total_allocated': len(allocations),
            'quota_fulfillment': quota_stats,
            'status': 'optimal' if prob.status == 1 else 'suboptimal'
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