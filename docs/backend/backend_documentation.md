# Backend Documentation

## Architecture

The backend of the Movie Recommender System is built using Flask, a lightweight Python web framework. It follows a modular structure to ensure maintainability and scalability.

## Directory Structure

```
movie_recommender_SVD/
├── main.py                      # Application entry point
├── .flaskenv                    # Flask environment variables
├── config.py                    # Configuration settings
├── application/                 # Main application package
│   ├── __init__.py              # Application factory
│   ├── routes.py                # Route definitions
│   ├── models.py                # Database models
│   ├── forms.py                 # Form definitions
│   ├── static/                  # Static files (CSS, JS, etc.)
│   └── templates/               # Jinja2 templates
├── models/                      # Saved ML models
└── utils/                       # Utility functions
```

## Core Components

### Application Factory

The application is created using the application factory pattern, which allows for multiple instances of the app and simplifies testing.

```python
# application/__init__.py
from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from application import routes
    
    return app
```

### Configuration

The application's configuration is managed through a dedicated config module, which allows for different environments (development, testing, production).

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DB', 'movie_recommender'),
        'host': os.environ.get('MONGO_URI', 'mongodb://localhost:27017/movie_recommender')
    }
    # Other configuration variables
```

### Routes

Routes define the URL structure of the application and handle incoming HTTP requests.

```python
# application/routes.py
from flask import render_template, redirect, url_for, flash, session
from application import app
from application.forms import LoginForm
from application.models import User, Movie, Rating, Prediction

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalog')
def catalog():
    movies = Movie.objects.all()
    return render_template('catalog.html', movies=movies)

# Additional routes for login, reviews, recommendations, etc.
```

### Database Models

MongoDB models define the structure of the data stored in the database using MongoEngine ODM (Object Document Mapper).

```python
# application/models.py
from application import db
from flask_security import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document, UserMixin):
    customer_id = db.StringField(required=True, unique=True)
    name = db.StringField(max_length=50)
    surname = db.StringField(max_length=50)
    email = db.EmailField(unique=True)
    password_hash = db.StringField()
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Movie(db.Document):
    movie_id = db.StringField(required=True, unique=True)
    title = db.StringField(required=True)
    genres = db.ListField(db.StringField())
    release_date = db.DateTimeField()
    # Additional movie fields

class Rating(db.Document):
    user = db.ReferenceField(User)
    movie = db.ReferenceField(Movie)
    rating = db.FloatField(min_value=0, max_value=5)
    timestamp = db.DateTimeField()
    
    meta = {
        'indexes': [
            {'fields': ['user', 'movie'], 'unique': True}
        ]
    }

class Prediction(db.Document):
    user = db.ReferenceField(User)
    movie = db.ReferenceField(Movie)
    predicted_rating = db.FloatField(min_value=0, max_value=5)
    
    meta = {
        'indexes': [
            {'fields': ['user', 'predicted_rating'], 'sparse': True}
        ]
    }
```

### Forms

Forms are built using Flask-WTF, which provides CSRF protection and validation.

```python
# application/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

# Additional forms for registration, rating movies, etc.
```

## API Endpoints

The application provides the following endpoints:

| Endpoint             | HTTP Method | Description                                   |
|----------------------|-------------|-----------------------------------------------|
| /                    | GET         | Home page                                     |
| /catalog             | GET         | Browse all movies                             |
| /login               | GET, POST   | User login                                    |
| /logout              | GET         | User logout                                   |
| /reviews             | GET         | View user's movie ratings                     |
| /recommend           | GET         | View personalized recommendations             |
| /rate/<movie_id>     | POST        | Submit a rating for a movie                   |

## Session Management

User sessions are managed using Flask's built-in session functionality, which stores session data in signed cookies. When a user logs in, their information is stored in the session for subsequent requests.

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = str(user.id)
            session['user_name'] = user.name
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)
```

## MongoDB Integration

MongoDB integration is handled through Flask-MongoEngine, which provides an ODM (Object Document Mapper) to interact with the database.

### Connection Setup

```python
# application/__init__.py
from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # Initialize MongoDB connection
    db.init_app(app)
    
    # Rest of the application setup
    
    return app
```

### Aggregation Pipelines

For complex queries like retrieving user ratings with movie details or generating recommendations, MongoDB aggregation pipelines are used:

```python
def get_user_ratings(user_id):
    pipeline = [
        {'$match': {'user': user_id}},
        {'$lookup': {
            'from': 'movie',
            'localField': 'movie',
            'foreignField': '_id',
            'as': 'movie_details'
        }},
        {'$unwind': '$movie_details'},
        {'$sort': {'movie_details.title': 1}}
    ]
    return list(Rating.objects.aggregate(pipeline))
```

## Error Handling

The application implements error handling to provide appropriate responses for different types of errors:

```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
```

## Authentication

User authentication is implemented using password hashing and session management:

1. Passwords are hashed using Werkzeug's security functions
2. Login credentials are validated against the database
3. User information is stored in the session upon successful login
4. Protected routes check for valid session data before allowing access

## Development and Deployment

### Development Setup

For local development, the application uses the `.flaskenv` file to configure the environment:

```
FLASK_APP=main.py
FLASK_ENV=development
FLASK_RUN_PORT=8081
```

### Deployment Considerations

For production deployment:

1. Set `FLASK_ENV=production`
2. Use a production-ready WSGI server (Gunicorn, uWSGI)
3. Set up proper logging
4. Configure HTTPS
5. Use environment variables for sensitive information 