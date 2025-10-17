# EcoLearn - Gamified Environmental Education Platform

EcoLearn is a comprehensive web application that makes environmental education fun and engaging through gamification, interactive lessons, real-world challenges, and a rewards system.

## 🌟 Features

- **User Authentication**: Separate registration for students and teachers
- **Interactive Lessons**: Environmental education content with quizzes
- **Real-world Challenges**: Eco-friendly activities with point rewards
- **Gamification System**: Points, badges, leaderboards, and progress tracking
- **Dual Dashboards**: Personalized views for students and teachers
- **Rewards System**: Digital badges and eco-points
- **Responsive Design**: Mobile-friendly with eco-themed styling

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd your-project-directory
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser to `http://localhost:5000`
   - Register as a student or teacher
   - Start learning and earning rewards!

## 📁 Project Structure

```
ecolearn/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── database/
│   └── init_db.py        # Database initialization
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── lessons.html
│   ├── quiz.html
│   ├── challenges.html
│   ├── leaderboard.html
│   ├── rewards.html
│   └── dashboard.html
└── static/               # Static assets
    ├── css/
    │   ├── style.css
    │   └── animations.css
    ├── js/
    │   ├── main.js
    │   ├── quiz.js
    │   ├── challenges.js
    │   └── dashboard.js
    └── images/
        └── logo.png
```

## 🗄️ Database Models

- **User**: Students and teachers with authentication and points
- **Lesson**: Educational content with categories and difficulty levels
- **Quiz**: Interactive assessments with multiple choice questions
- **Challenge**: Real-world eco activities
- **UserProgress**: Lesson completion tracking
- **UserChallenge**: Challenge participation tracking
- **Badge**: Achievement rewards
- **UserBadge**: Earned badges tracking

## 🌐 API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Learning
- `GET /lessons` - View all lessons
- `GET /lesson/<id>` - View lesson details
- `GET /quiz/<id>` - Take lesson quiz
- `POST /submit_quiz/<id>` - Submit quiz answers

### Challenges
- `GET /challenges` - View available challenges
- `GET /join_challenge/<id>` - Join a challenge
- `POST /complete_challenge/<id>` - Mark challenge complete

### Social & Analytics
- `GET /leaderboard` - View points leaderboard
- `GET /rewards` - View earned badges
- `GET /dashboard` - Personal progress dashboard
- `GET /api/user_progress` - Progress data (JSON)

## 🚀 Deployment Options

### Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-ecolearn-app
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   ```

5. **Initialize database**
   ```bash
   heroku run python database/init_db.py
   ```

### Local Development with Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] User registration (student and teacher)
- [ ] User login/logout
- [ ] Lesson browsing and starting
- [ ] Quiz taking and scoring
- [ ] Challenge joining and completion
- [ ] Points earning and badge unlocking
- [ ] Leaderboard viewing
- [ ] Dashboard data accuracy
- [ ] Responsive design on mobile devices

### Automated Testing (Future Enhancement)
```bash
# Install testing dependencies
pip install pytest flask-testing

# Run tests
pytest
```

## 🔧 Configuration

Edit `config.py` to customize:
- Database URI
- Secret key
- Other Flask settings

## 🎨 Customization

### Adding New Lessons
1. Add lesson data to `app.py` in the `create_tables()` function
2. Include quiz questions with options and correct answers

### Adding New Challenges
1. Add challenge data to the sample data initialization
2. Update challenge completion logic if needed

### Styling
- Main styles: `static/css/style.css`
- Animations: `static/css/animations.css`
- Colors use CSS custom properties for easy theming

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions or issues, please check the code comments or create an issue in the repository.

---

**Happy Learning! 🌱 Make a positive impact on our planet through education and action.**
