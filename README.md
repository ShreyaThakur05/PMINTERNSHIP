# 🎓 AI-Powered Internship Allocation System

An intelligent system that automatically allocates internship positions to students while ensuring government quota compliance and optimal matching.

## 🚀 Features

- **AI-Powered Matching**: Uses machine learning to match students with internships based on skills, preferences, and qualifications
- **Quota Compliance**: Automatically enforces government quotas (SC: 15%, ST: 7.5%, OBC: 27%, Aspirational Districts: 20%)
- **Optimization Algorithm**: Uses Integer Linear Programming to find globally optimal allocations
- **Web Dashboard**: Interactive frontend for monitoring and controlling the allocation process
- **MongoDB Atlas Integration**: Cloud database for scalable data storage

## 📋 Requirements

- Python 3.8+
- MongoDB Atlas account (free tier available)
- Internet connection for ML model downloads

## 🛠️ Quick Start

1. **Clone and Setup**:
   ```bash
   cd pminternship
   python run_system.py
   ```

2. **Configure Database**:
   - Create a MongoDB Atlas account at https://www.mongodb.com/atlas
   - Create a new cluster (free tier is sufficient)
   - Get your connection string
   - Update `.env` file with your MongoDB URI

3. **Run the System**:
   - The system will automatically install dependencies
   - Generate sample data (1000 students, 100 internships)
   - Start the API server
   - Open the web dashboard

## 🎯 How It Works

### Step 1: Data Processing
- Loads student and internship data from CSV files
- Extracts features like skills, location preferences, academic performance
- Generates embeddings for semantic matching

### Step 2: ML Matching
- Calculates match scores between students and internships
- Uses XGBoost for intelligent scoring (falls back to weighted scoring)
- Considers skills, location, sector preferences, and academic fit

### Step 3: Optimization
- Formulates as Integer Linear Programming problem
- Maximizes total match quality while enforcing constraints:
  - Each student gets at most one internship
  - Internship capacity limits
  - Government quota requirements
  - Geographic distribution preferences

### Step 4: Results
- Provides optimal allocation with quota compliance
- Shows detailed analytics and fairness metrics
- Generates audit trails for transparency

## 📊 Government Quota Implementation

For 1000 internships, the system ensures:
- **SC (Scheduled Caste)**: Minimum 150 positions (15%)
- **ST (Scheduled Tribe)**: Minimum 75 positions (7.5%)
- **OBC (Other Backward Classes)**: Minimum 270 positions (27%)
- **Aspirational Districts**: Minimum 200 positions (20%)

## 🔧 API Endpoints

- `POST /api/load-data` - Load data from CSV files
- `POST /api/allocate` - Run allocation algorithm
- `GET /api/students` - Get all students
- `GET /api/internships` - Get all internships
- `GET /api/stats` - Get system statistics
- `POST /api/match-score` - Calculate match score for student-internship pair

## 📁 Project Structure

```
pminternship/
├── app.py                 # Flask API server
├── database.py           # MongoDB Atlas integration
├── ml_engine.py          # Machine learning matching engine
├── allocation_optimizer.py # ILP optimization algorithm
├── config.py             # System configuration
├── datasetcode.py        # Sample data generation
├── frontend.html         # Web dashboard
├── run_system.py         # Main system runner
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── README.md            # This file
```

## 🎨 Web Dashboard Features

- **System Controls**: Load data, run allocation, refresh statistics
- **Real-time Statistics**: Student counts, internship availability, capacity
- **Visual Analytics**: Category distribution charts, quota fulfillment bars
- **Allocation Results**: Detailed allocation list with match scores
- **Quota Monitoring**: Real-time quota compliance tracking

## 🔍 Technical Details

### Machine Learning Pipeline
- **Feature Engineering**: Extracts 10+ features per student-internship pair
- **Embedding Generation**: Uses Sentence Transformers for semantic similarity
- **XGBoost Model**: Trained on historical allocation success data
- **Fallback Scoring**: Weighted scoring when ML model unavailable

### Optimization Engine
- **Algorithm**: Integer Linear Programming using PuLP
- **Objective**: Maximize total match quality
- **Constraints**: Capacity limits, quota requirements, fairness rules
- **Solver**: CBC (Coin-or Branch and Cut) solver

### Database Schema
- **Students Collection**: Personal info, skills, preferences, social category
- **Internships Collection**: Company details, requirements, capacity
- **Allocations Collection**: Historical allocation results and analytics

## 🚀 Deployment Options

### Local Development
```bash
python run_system.py
```

### Production Deployment
- Use Docker containers for scalability
- Deploy API server on cloud platforms (AWS, GCP, Azure)
- Use MongoDB Atlas for production database
- Implement load balancing for high availability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section below
2. Create an issue on GitHub
3. Contact the development team

## 🔧 Troubleshooting

### Common Issues

**MongoDB Connection Error**:
- Ensure your MongoDB Atlas cluster is running
- Check your connection string in `.env`
- Verify network access (whitelist your IP)

**Package Installation Errors**:
- Update pip: `python -m pip install --upgrade pip`
- Use virtual environment: `python -m venv venv`

**Port Already in Use**:
- Change port in `config.py`
- Kill existing processes: `netstat -ano | findstr :5000`

**Memory Issues with Large Datasets**:
- Reduce batch size in ML processing
- Use data streaming for large CSV files
- Consider upgrading system RAM

## 🎯 Future Enhancements

- [ ] Real-time allocation updates
- [ ] Advanced bias detection algorithms
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Integration with external HR systems
- [ ] Predictive analytics for workforce planning
- [ ] Advanced reporting and dashboards
- [ ] API rate limiting and authentication