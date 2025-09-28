from flask import Flask, request, jsonify
from flask_cors import CORS
from local_database import LocalDatabaseManager
from ml_engine import MatchingEngine
from simple_allocator import SimpleAllocator
import datetime

app = Flask(__name__)
CORS(app)

# Initialize components
db_manager = LocalDatabaseManager()
matching_engine = MatchingEngine()
allocator = SimpleAllocator()

@app.route('/api/load-data', methods=['POST'])
def load_data():
    """Load student and internship data from CSV files"""
    try:
        students_count = db_manager.load_students_from_csv()
        internships_count = db_manager.load_internships_from_csv()
        
        return jsonify({
            'success': True,
            'message': f'Loaded {students_count} students and {internships_count} internships',
            'students_count': students_count,
            'internships_count': internships_count
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/allocate', methods=['POST'])
def allocate_internships():
    """Run the allocation algorithm"""
    try:
        # Get data from database
        students = db_manager.get_students()
        internships = db_manager.get_internships()
        
        if not students or not internships:
            return jsonify({'success': False, 'error': 'No data found. Please load data first.'}), 400
        
        # Calculate match scores
        match_scores = {}
        for i, student in enumerate(students):
            for j, internship in enumerate(internships):
                score = matching_engine.calculate_match_score(student, internship)
                match_scores[(i, j)] = score
        
        # Run allocation
        result = allocator.allocate(students, internships, match_scores)
        
        # Save allocation to database (simplified)
        try:
            allocation_data = {
                'timestamp': datetime.datetime.utcnow().isoformat(),
                'total_students': len(students),
                'total_internships': len(internships),
                'total_allocated': result['total_allocated']
            }
            db_manager.save_allocation(allocation_data)
        except Exception as e:
            print(f"Warning: Could not save allocation: {e}")
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        students = db_manager.get_students()
        # Students already in correct format
        return jsonify({'success': True, 'students': students})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/internships', methods=['GET'])
def get_internships():
    """Get all internships"""
    try:
        internships = db_manager.get_internships()
        # Internships already in correct format
        return jsonify({'success': True, 'internships': internships})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/match-score', methods=['POST'])
def calculate_match_score():
    """Calculate match score between a student and internship"""
    try:
        data = request.json
        student_id = data.get('student_id')
        internship_id = data.get('internship_id')
        
        students = db_manager.get_students()
        internships = db_manager.get_internships()
        
        student = next((s for s in students if s['student_id'] == student_id), None)
        internship = next((i for i in internships if i['internship_id'] == internship_id), None)
        
        if not student or not internship:
            return jsonify({'success': False, 'error': 'Student or internship not found'}), 404
        
        score = matching_engine.calculate_match_score(student, internship)
        features = matching_engine.extract_features(student, internship)
        
        return jsonify({
            'success': True,
            'match_score': score,
            'features': features
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        students = db_manager.get_students()
        internships = db_manager.get_internships()
        
        # Calculate category distribution
        category_counts = {'SC': 0, 'ST': 0, 'OBC': 0, 'GEN': 0}
        rural_count = 0
        aspirational_count = 0
        
        for student in students:
            category = student['social_category']['category']
            category_counts[category] += 1
            
            if student['social_category']['is_rural']:
                rural_count += 1
            if student['social_category']['is_aspirational_district']:
                aspirational_count += 1
        
        # Calculate sector distribution
        sector_counts = {}
        total_capacity = 0
        for internship in internships:
            sector = internship['sector']
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
            total_capacity += internship['capacity']
        
        return jsonify({
            'success': True,
            'stats': {
                'total_students': len(students),
                'total_internships': len(internships),
                'total_capacity': total_capacity,
                'category_distribution': category_counts,
                'rural_students': rural_count,
                'aspirational_district_students': aspirational_count,
                'sector_distribution': sector_counts
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.datetime.utcnow().isoformat()})

@app.route('/', methods=['GET'])
def home():
    """Redirect to frontend"""
    return '<h1>AI Internship Allocation API</h1><p>API is running. Open <a href="enhanced_frontend.html">enhanced_frontend.html</a> to use the system.</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)