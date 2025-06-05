from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from datetime import datetime, UTC

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.context_processor
def inject_now():
    """Add current year to all templates."""
    return {'now': datetime.now(UTC)}

# =====================================================================
# TEMPORARY DUMMY DATA
# This data will be replaced with SQLite database queries in Phase 4
# =====================================================================

# Dummy data for a specific user (user_id: 1132304)
# This follows the format from the guide and Netflix Prize dataset
ratings_ = [
    {
        "user_id": "1132304", 
        "movie_id": "1", 
        "movie_title": "Toy Story", 
        "rating": 5.0, 
        "timestamp": 964982703
    },
    {
        "user_id": "1132304", 
        "movie_id": "780", 
        "movie_title": "Independence Day", 
        "rating": 4.0, 
        "timestamp": 964981247
    },
    {
        "user_id": "1132304", 
        "movie_id": "590", 
        "movie_title": "Dances with Wolves", 
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
        "est_rating": 4.95
    },
    {
        "user_id": "1132304", 
        "movie_id": "1240", 
        "movie_title": "Terminator, The", 
        "est_rating": 4.89
    },
    {
        "user_id": "1132304", 
        "movie_id": "1196", 
        "movie_title": "Star Wars: Episode V - The Empire Strikes Back", 
        "est_rating": 4.88
    }
]

# Dummy movie catalog data
movies_ = [
    {
        "movie_id": "1",
        "title": "Toy Story"
    },
    {
        "movie_id": "2",
        "title": "Jumanji"
    },
    {
        "movie_id": "3",
        "title": "Grumpier Old Men"
    },
    {
        "movie_id": "4",
        "title": "Waiting to Exhale"
    },
    {
        "movie_id": "5",
        "title": "Father of the Bride Part II"
    }
]

# Additional movie information (this would typically come from a separate dataset)
# This is used to enhance the display but isn't part of the core Netflix dataset
movie_info = {
    "1": {"year": 1995, "genres": ["Animation", "Children", "Comedy"]},
    "2": {"year": 1995, "genres": ["Adventure", "Children", "Fantasy"]},
    "3": {"year": 1995, "genres": ["Comedy", "Romance"]},
    "4": {"year": 1995, "genres": ["Comedy", "Drama"]},
    "5": {"year": 1995, "genres": ["Comedy"]}
}

# =====================================================================
# END OF TEMPORARY DUMMY DATA
# =====================================================================

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
    
    # TODO: Replace with SQLite database queries in Phase 4
    # Use the dummy movie data and enhance with additional info
    movies = []
    for movie in movies_:
        movie_id = movie["movie_id"]
        enhanced_movie = {
            "movie_id": movie_id,
            "title": movie["title"]
        }
        
        # Add additional info if available
        if movie_id in movie_info:
            enhanced_movie["year"] = movie_info[movie_id]["year"]
            enhanced_movie["genres"] = movie_info[movie_id]["genres"]
        
        # Calculate average rating (in a real app, this would come from the database)
        enhanced_movie["avg_rating"] = 3.5  # Default placeholder
        
        movies.append(enhanced_movie)
    
    # Filter by genre if specified
    if genre:
        movies = [m for m in movies if "genres" in m and genre.lower() in [g.lower() for g in m["genres"]]]
    
    # Filter by search term if specified
    if search:
        movies = [m for m in movies if search.lower() in m["title"].lower()]
    
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
        
        # TODO: Replace with proper authentication in Phase 6
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
    
    # TODO: Replace with SQLite database queries in Phase 4
    # Filter ratings for the logged-in user
    user_ratings = [r for r in ratings_ if r['user_id'] == user_id]
    
    # Convert timestamp to datetime for display
    for rating in user_ratings:
        rating['date_rated'] = datetime.fromtimestamp(rating['timestamp'], UTC)
        
        # Add additional movie info for display purposes
        movie_id = rating['movie_id']
        if movie_id in movie_info:
            rating['movie_year'] = movie_info[movie_id]['year']
            rating['movie_genres'] = movie_info[movie_id]['genres']
    
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
    
    # TODO: Replace with SQLite database queries and SVD model in Phase 7
    # Filter recommendations for the logged-in user
    user_recommendations = [p for p in preds_ if p['user_id'] == user_id]
    
    # Prepare data for the template
    personalized_recommendations = []
    for rec in user_recommendations:
        movie_id = rec['movie_id']
        recommendation = {
            'movie_id': movie_id,
            'movie_title': rec['movie_title'],
            'match_percentage': int(rec['est_rating'] * 20)  # Convert 5-star rating to percentage
        }
        
        # Add additional movie info for display purposes
        if movie_id in movie_info:
            recommendation['movie_year'] = movie_info[movie_id]['year'] if movie_id in movie_info else 1995
            recommendation['movie_genres'] = movie_info[movie_id]['genres'] if movie_id in movie_info else []
        
        # Add a description (this would come from a separate dataset in a real app)
        recommendation['description'] = f"Recommended based on your ratings. Estimated rating: {rec['est_rating']}/5."
        
        personalized_recommendations.append(recommendation)
    
    # Dummy popular recommendations
    popular_recommendations = [
        {
            'movie_id': '356',
            'movie_title': 'Forrest Gump',
            'movie_year': 1994,
            'movie_genres': ['Comedy', 'Drama', 'Romance'],
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
