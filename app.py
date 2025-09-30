from flask import Flask, request, jsonify
from flask_cors import CORS
from local_database import LocalDatabaseManager
from ml_engine import MatchingEngine
from simple_allocator import SimpleAllocator
from rag_chatbot import RAGChatbot
import datetime
import json

app = Flask(__name__)
CORS(app)

# Initialize components
db_manager = LocalDatabaseManager()
matching_engine = MatchingEngine()
allocator = SimpleAllocator()
chatbot = RAGChatbot()

@app.route('/api/load-data', methods=['POST'])
def load_data():
    """Load student and internship data from CSV files or generate sample data"""
    try:
        # Check if CSV files exist, if not generate them
        import os
        if not os.path.exists('students.csv') or not os.path.exists('internships.csv'):
            print("CSV files not found, generating sample data...")
            from datasetcode import generate_sample_data
            generate_sample_data()
        
        students_count = db_manager.load_students_from_csv()
        internships_count = db_manager.load_internships_from_csv()
        
        return jsonify({
            'success': True,
            'message': f'Loaded {students_count} students and {internships_count} internships',
            'students_count': students_count,
            'internships_count': internships_count
        })
    except Exception as e:
        print(f"Error in load_data: {e}")
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
        
        # Save all allocations at once
        try:
            allocations_with_flag = []
            for allocation in result['allocations']:
                allocation['allocated'] = True
                allocations_with_flag.append(allocation)
            
            # Use database manager for consistent file handling
            with open(db_manager.allocations_file, 'w') as f:
                json.dump(allocations_with_flag, f, indent=2)
            print(f"Saved {len(result['allocations'])} allocations to {db_manager.allocations_file}")
        except Exception as e:
            print(f"Error saving allocations: {e}")
        
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
        
        print(f"Stats: Found {len(students)} students, {len(internships)} internships")
        
        # Calculate category distribution
        category_counts = {'SC': 0, 'ST': 0, 'OBC': 0, 'GEN': 0}
        rural_count = 0
        aspirational_count = 0
        
        for student in students:
            category = student.get('social_category', {}).get('category', 'GEN')
            if category in category_counts:
                category_counts[category] += 1
            
            if student.get('social_category', {}).get('is_rural', False):
                rural_count += 1
            if student.get('social_category', {}).get('is_aspirational_district', False):
                aspirational_count += 1
        
        # Calculate sector distribution
        sector_counts = {}
        total_capacity = 0
        for internship in internships:
            sector = internship.get('sector', 'Unknown')
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
            total_capacity += internship.get('capacity', 0)
        
        stats = {
            'total_students': len(students),
            'total_internships': len(internships),
            'total_capacity': total_capacity,
            'category_distribution': category_counts,
            'rural_students': rural_count,
            'aspirational_district_students': aspirational_count,
            'sector_distribution': sector_counts
        }
        
        print(f"Returning stats: {stats}")
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        print(f"Error in get_stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        students = db_manager.get_students()
        internships = db_manager.get_internships()
        allocations = db_manager.get_allocations()
        
        return jsonify({
            'status': 'healthy', 
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'data_status': {
                'students_loaded': len(students),
                'internships_loaded': len(internships),
                'allocations_made': len(allocations)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """RAG Chatbot endpoint"""
    try:
        data = request.json
        question = data.get('question', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
            
        response = chatbot.query(question)
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Redirect to frontend"""
    return '<h1>AI Internship Allocation API</h1><p>API is running. Open <a href="enhanced_frontend.html">enhanced_frontend.html</a> to use the system.</p>'

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)