# 🎓 Education Career Analysis System

A Flask-based web application that provides personalized career, education, and TESDA course recommendations using machine learning.

## ✨ Features

- 👤 User authentication (Register/Login)
- 🎯 Personalized career pathway recommendations
- 📚 Education pathway suggestions (SHS, College, ALS)
- 🔧 TESDA technical course recommendations
- 💾 Save and bookmark recommendations
- 📊 ML-based matching with 5 top recommendations
- 🎨 Modern, responsive UI

## 🚀 Quick Start

### Local Development

1. **Clone and setup:**

   ```bash
   cd education_system
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```
   Visit: http://localhost:5000

### Deployment Options

**Choose one:**

| Platform           | Link                                                                 | Time   |
| ------------------ | -------------------------------------------------------------------- | ------ |
| **Heroku**         | [See DEPLOYMENT.md](DEPLOYMENT.md#option-1-deploy-to-heroku)         | 5 min  |
| **PythonAnywhere** | [See DEPLOYMENT.md](DEPLOYMENT.md#option-2-deploy-to-pythonanywhere) | 5 min  |
| **Railway**        | [See DEPLOYMENT.md](DEPLOYMENT.md#option-3-deploy-to-railway)        | 5 min  |
| **DigitalOcean**   | [See DEPLOYMENT.md](DEPLOYMENT.md#option-4-deploy-to-digitalocean)   | 15 min |

## 📁 Project Structure

```
education_system/
├── app.py                 # Main Flask application
├── ml_model.py            # ML model loading and prediction
├── requirements.txt       # Python dependencies
├── Procfile              # Deployment config (Heroku)
├── education_system.db   # SQLite database
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── pathway_career.html
│   ├── pathway_education.html
│   ├── pathway_tesda.html
│   ├── my_recommendations.html
│   └── profile.html
├── static/
│   ├── style.css         # Main stylesheet
│   └── pathway.js        # Frontend logic
└── models/
    ├── model_career.pkl
    ├── model_education.pkl
    └── model_tesda.pkl
```

## 🔐 Authentication

- Secure password hashing with Werkzeug
- Session-based authentication
- User profile management

## 🤖 Machine Learning

Three independent RandomForestClassifier models:

- **Career**: Predicts job titles based on skills, industry, salary, environment
- **Education**: Recommends programs (SHS/College/ALS) based on preferences
- **TESDA**: Suggests technical courses based on interests and availability

**Filtering System**:

- Keyword-based scoring for accuracy
- Top 5 results per pathway
- Dynamic metadata display

## 📊 Database Schema

**Users:**

- user_id, username, password_hash, created_at

**Profiles:**

- user_id, age, education_level, career_interest, etc.

**Recommendations:**

- id, user_id, pathway, recommendation_data, saved, created_at

## 🎯 Usage

1. **Register** - Create new account
2. **Login** - Access dashboard
3. **Explore Pathways**:
   - Career (select industry, skills, salary range)
   - Education (select program type and preferences)
   - TESDA (select course interest and availability)
4. **View Recommendations** - See top 5 personalized suggestions
5. **Save Recommendations** - Bookmark for later reference
6. **My Recommendations** - View all saved recommendations

## 🛠️ Development

### Technologies Used

- **Backend**: Flask 3.1.0, Python 3.11
- **ML**: scikit-learn, pandas, numpy
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite3
- **Deployment**: Heroku, PythonAnywhere, Railway, etc.

### Key Dependencies

```
Flask==3.1.0
scikit-learn==1.6.1
pandas>=2.0.0
numpy>=1.26.0
gunicorn==21.2.0
joblib>=1.3.0
```

## 📝 Configuration

For production deployment, set environment variables:

```bash
export DEBUG=False
export SECRET_KEY=your-secure-key-here
```

## 🚨 Important Notes

- Change `DEBUG=False` in production
- Use strong secret keys
- Consider PostgreSQL for production database
- Enable HTTPS on deployed server
- Set up regular backups

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT.md) - Step-by-step deployment instructions
- [API Routes](docs/ROUTES.md) - Available endpoints
- [User Guide](docs/USER_GUIDE.md) - How to use the application

## 👨‍💻 Author

Created with ❤️ for career guidance

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:

1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
2. Review error logs
3. Ensure all dependencies are installed

---

**Ready to deploy?** → Check [DEPLOYMENT.md](DEPLOYMENT.md)
