"""
Data Loader Module

This module provides functions to load and process data from the CSV files.
"""

import os
import pandas as pd
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
ML_DATA_DIR = DATA_DIR / 'ml-latest-small'
TMDB_DATA_DIR = DATA_DIR / 'tmdb_metadata'

# Data file paths
MOVIES_FILE = ML_DATA_DIR / 'movies.csv'
RATINGS_FILE = ML_DATA_DIR / 'ratings.csv'
LINKS_FILE = ML_DATA_DIR / 'links.csv'
TAGS_FILE = ML_DATA_DIR / 'tags.csv'
POSTER_LINKS_FILE = TMDB_DATA_DIR / 'poster_links.csv'
CAST_CREW_FILE = TMDB_DATA_DIR / 'movie_cast_and_crew.csv'

def check_data_files():
    """Check if all required data files exist."""
    required_files = [
        MOVIES_FILE,
        RATINGS_FILE,
        LINKS_FILE,
        TAGS_FILE,
        POSTER_LINKS_FILE,
        CAST_CREW_FILE
    ]
    
    missing_files = [f for f in required_files if not f.exists()]
    
    if missing_files:
        missing_files_str = '\n'.join(str(f) for f in missing_files)
        raise FileNotFoundError(
            f"Missing required data files:\n{missing_files_str}\n"
            f"Please run scripts/setup_data.py to extract the data files."
        )
    
    return True

def load_movies():
    """Load and process the movies data."""
    check_data_files()
    
    # Load movies
    movies_df = pd.read_csv(MOVIES_FILE)
    
    # Process genres: Split the '|' separated string into a list
    movies_df['genres'] = movies_df['genres'].apply(
        lambda x: x.split('|') if x != '(no genres listed)' else []
    )
    
    # Extract year from title
    movies_df['year'] = movies_df['title'].str.extract(r'\((\d{4})\)$')
    movies_df['title'] = movies_df['title'].str.replace(r'\s*\(\d{4}\)$', '', regex=True)
    
    return movies_df

def load_ratings():
    """Load and process the ratings data."""
    check_data_files()
    
    # Load ratings
    ratings_df = pd.read_csv(RATINGS_FILE)
    
    return ratings_df

def load_poster_links():
    """Load and process the poster links data."""
    check_data_files()
    
    # Load poster links
    poster_links_df = pd.read_csv(POSTER_LINKS_FILE)
    
    return poster_links_df

def load_cast_and_crew():
    """Load and process the cast and crew data."""
    check_data_files()
    
    # Load cast and crew data
    cast_crew_df = pd.read_csv(CAST_CREW_FILE)
    
    return cast_crew_df

def get_movie_metadata(movie_id):
    """Get all metadata for a specific movie."""
    # Load all required dataframes
    movies_df = load_movies()
    poster_links_df = load_poster_links()
    
    # Filter for the specific movie
    movie_data = movies_df[movies_df['movieId'] == movie_id].iloc[0].to_dict() if not movies_df[movies_df['movieId'] == movie_id].empty else None
    
    if movie_data:
        # Add poster link if available
        poster_data = poster_links_df[poster_links_df['movieId'] == movie_id]
        if not poster_data.empty:
            movie_data['poster_link'] = poster_data.iloc[0]['poster_link']
        else:
            movie_data['poster_link'] = None
    
    return movie_data

def get_user_ratings(user_id):
    """Get all ratings for a specific user."""
    # Load ratings
    ratings_df = load_ratings()
    
    # Filter for the specific user
    user_ratings = ratings_df[ratings_df['userId'] == user_id]
    
    # Get movie details for each rating
    result = []
    for _, rating in user_ratings.iterrows():
        movie_data = get_movie_metadata(rating['movieId'])
        if movie_data:
            result.append({
                'user_id': str(rating['userId']),
                'movie_id': str(rating['movieId']),
                'movie_title': movie_data['title'],
                'rating': rating['rating'],
                'timestamp': rating['timestamp']
            })
    
    return result

def get_movie_recommendations(user_id, n=10):
    """
    Get movie recommendations for a specific user.
    This is a placeholder that will be replaced by the SVD model.
    """
    # Load movies
    movies_df = load_movies()
    
    # For now, just return some random movies
    # This will be replaced by the SVD model later
    import random
    random_movies = movies_df.sample(n)
    
    # Format the results
    result = []
    for _, movie in random_movies.iterrows():
        result.append({
            'user_id': str(user_id),
            'movie_id': str(movie['movieId']),
            'movie_title': movie['title'],
            'est_rating': round(random.uniform(3.5, 5.0), 2)
        })
    
    return result 