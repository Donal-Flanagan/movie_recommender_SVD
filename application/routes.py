from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from datetime import datetime, UTC

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.context_processor
def inject_now():
    """Add current year to all templates."""
    return {'now': datetime.now(UTC)}

# Dummy data for a specific user (user_id: 1132304)
# This follows the format from the guide
ratings_ = [
    {
        "user_id": "1132304",
        "movie_id": "1",
        "movie_title": "Toy Story",
        "movie_genres": ["Adventure", "Animation", "Children", "Comedy", "Fantasy"],
        "rating": 5.0,
        "timestamp": 964982703
    },
    {
        "user_id": "1132304",
        "movie_id": "780",
        "movie_title": "Independence Day",
        "movie_genres": ["Action", "Adventure", "Sci-Fi", "Thriller"],
        "rating": 4.0,
        "timestamp": 964981247
    },
    {
        "user_id": "1132304",
        "movie_id": "590",
        "movie_title": "Dances with Wolves",
        "movie_genres": ["Adventure", "Drama", "Western"],
        "rating": 4.0,
        "timestamp": 964982224
    }
]

# Dummy recommendation data
preds_ = [
    {
        "user_id": "1132304",
        "movie_id": "589",
        "movie_title": "Terminator 2: Judgment Day",
        "movie_genres": ["Action", "Sci-Fi", "Thriller"],
        "est_rating": 4.95,
        "match_percentage": 99
    },
    {
        "user_id": "1132304",
        "movie_id": "1240",
        "movie_title": "Terminator, The",
        "movie_genres": ["Action", "Sci-Fi", "Thriller"],
        "est_rating": 4.89,
        "match_percentage": 98
    },
    {
        "user_id": "1132304",
        "movie_id": "1196",
        "movie_title": "Star Wars: Episode V - The Empire Strikes Back",
        "movie_genres": ["Action", "Adventure", "Drama", "Sci-Fi", "War"],
        "est_rating": 4.88,
        "match_percentage": 98
    }
]

# Dummy movie catalog data
movies_ = [
    {
        "movie_id": "1",
        "title": "Toy Story",
        "genres": ["Adventure", "Animation", "Children", "Comedy", "Fantasy"],
        "year": 1995,
        "avg_rating": 4.15
    },
    {
        "movie_id": "2",
        "title": "Jumanji",
        "genres": ["Adventure", "Children", "Fantasy"],
        "year": 1995,
        "avg_rating": 3.75
    },
    {
        "movie_id": "3",
        "title": "Grumpier Old Men",
        "genres": ["Comedy", "Romance"],
        "year": 1995,
        "avg_rating": 3.22
    },
    {
        "movie_id": "4",
        "title": "Waiting to Exhale",
        "genres": ["Comedy", "Drama", "Romance"],
        "year": 1995,
        "avg_rating": 2.88
    },
    {
        "movie_id": "5",
        "title": "Father of the Bride Part II",
        "genres": ["Comedy"],
        "year": 1995,
        "avg_rating": 3.05
    }
]

@main.route('/')
def index():
    """Homepage route"""
    return render_template('index.html', title='Home')

@main.route('/catalog')
def catalog():
    """Movie catalog route"""
    # Get query parameters for filtering and pagination
    page = request.args.get('page', 1, type=int)
    genre = request.args.get('genre', None)
    search = request.args.get('search', None)
    
    # Use the dummy movie data
    movies = movies_
    
    # Filter by genre if specified
    if genre:
        movies = [m for m in movies if genre.lower() in [g.lower() for g in m['genres']]]
    
    # Filter by search term if specified
    if search:
        movies = [m for m in movies if search.lower() in m['title'].lower()]
    
    # Pagination data
    pagination = {
        'current_page': page,
        'total_pages': 1,  # Just one page for now
        'has_prev': False,
        'has_next': False
    }
    
    return render_template('catalog.html', 
                          title='Movie Catalog',
                          movies=movies, 
                          pagination=pagination,
                          selected_genre=genre,
                          search_query=search)

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        # Simple login logic (to be replaced with actual authentication)
        if email == "user@example.com" and password == "password":
            # Set user in session
            session['user'] = {
                'user_id': '1132304',  # Using the same user_id as in our dummy data
                'name': 'John',
                'email': email
            }
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', title='Login')

@main.route('/logout')
def logout():
    """Logout route"""
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/reviews')
def reviews():
    """User ratings route"""
    # Check if user is logged in
    if 'user' not in session:
        flash('Please login to view your ratings.', 'warning')
        return redirect(url_for('main.login'))
    
    # Get user_id from session
    user_id = session['user']['user_id']
    
    # Filter ratings for the logged-in user
    user_ratings = [r for r in ratings_ if r['user_id'] == user_id]
    
    # Convert timestamp to datetime for display
    for rating in user_ratings:
        rating['date_rated'] = datetime.fromtimestamp(rating['timestamp'], UTC)
    
    return render_template('reviews.html', 
                          title='My Ratings',
                          ratings=user_ratings,
                          total_ratings=len(user_ratings))

@main.route('/recommend')
def recommend():
    """Movie recommendations route"""
    # Check if user is logged in
    if 'user' not in session:
        flash('Please login to view your recommendations.', 'warning')
        return redirect(url_for('main.login'))
    
    # Get user_id from session
    user_id = session['user']['user_id']
    
    # Filter recommendations for the logged-in user
    user_recommendations = [p for p in preds_ if p['user_id'] == user_id]
    
    # Prepare data for the template
    personalized_recommendations = []
    for rec in user_recommendations:
        personalized_recommendations.append({
            'movie_id': rec['movie_id'],
            'movie_title': rec['movie_title'],
            'movie_year': 1995,  # Placeholder, would come from movie metadata
            'movie_genres': rec['movie_genres'],
            'match_percentage': rec['match_percentage'],
            'description': f"A recommended movie based on your rating patterns. Estimated rating: {rec['est_rating']}/5."
        })
    
    # Dummy popular recommendations
    popular_recommendations = [
        {
            'movie_id': '356',
            'movie_title': 'Forrest Gump',
            'movie_year': 1994,
            'movie_genres': ['Comedy', 'Drama', 'Romance', 'War'],
            'rating': 4.5,
            'description': 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.'
        }
    ]
    
    return render_template('recommend.html', 
                          title='Your Recommendations',
                          personalized=personalized_recommendations,
                          popular=popular_recommendations)

@main.errorhandler(404)
def page_not_found(e):
    """404 error handler"""
    return render_template('errors/404.html'), 404

@main.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('errors/500.html'), 500
