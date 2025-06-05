#!/usr/bin/env python3
"""
Test Data Loader Script

This script tests the data_loader module to ensure it can access and process the data files.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the Python path so we can import the application module
sys.path.append(str(Path(__file__).resolve().parent.parent))

from application.data_loader import (
    check_data_files,
    load_movies,
    load_ratings,
    load_poster_links,
    load_cast_and_crew,
    get_movie_metadata,
    get_user_ratings,
    get_movie_recommendations
)

def test_check_data_files():
    """Test that all required data files are accessible."""
    print("Testing data file accessibility...")
    try:
        check_data_files()
        print("✅ All data files are accessible")
    except Exception as e:
        print(f"❌ Error checking data files: {e}")
        return False
    return True

def test_load_movies():
    """Test loading the movies data."""
    print("\nTesting movie data loading...")
    try:
        movies_df = load_movies()
        print(f"✅ Successfully loaded {len(movies_df)} movies")
        print("First 5 movies:")
        print(movies_df.head().to_string())
    except Exception as e:
        print(f"❌ Error loading movies: {e}")
        return False
    return True

def test_load_ratings():
    """Test loading the ratings data."""
    print("\nTesting ratings data loading...")
    try:
        ratings_df = load_ratings()
        print(f"✅ Successfully loaded {len(ratings_df)} ratings")
        print("First 5 ratings:")
        print(ratings_df.head().to_string())
    except Exception as e:
        print(f"❌ Error loading ratings: {e}")
        return False
    return True

def test_load_poster_links():
    """Test loading the poster links data."""
    print("\nTesting poster links data loading...")
    try:
        poster_links_df = load_poster_links()
        print(f"✅ Successfully loaded {len(poster_links_df)} poster links")
        print("First 5 poster links:")
        print(poster_links_df.head().to_string())
    except Exception as e:
        print(f"❌ Error loading poster links: {e}")
        return False
    return True

def test_get_movie_metadata():
    """Test retrieving metadata for a specific movie."""
    print("\nTesting movie metadata retrieval...")
    try:
        # Try to get metadata for Toy Story (movie ID 1)
        movie_data = get_movie_metadata(1)
        if movie_data:
            print(f"✅ Successfully retrieved metadata for movie: {movie_data['title']}")
            print(f"Year: {movie_data['year']}")
            print(f"Genres: {movie_data['genres']}")
            print(f"Poster link: {movie_data.get('poster_link', 'Not available')}")
        else:
            print("❌ Movie not found")
            return False
    except Exception as e:
        print(f"❌ Error retrieving movie metadata: {e}")
        return False
    return True

def test_get_user_ratings():
    """Test retrieving ratings for a specific user."""
    print("\nTesting user ratings retrieval...")
    try:
        # Try to get ratings for user ID 1
        user_ratings = get_user_ratings(1)
        print(f"✅ Successfully retrieved {len(user_ratings)} ratings for user 1")
        if user_ratings:
            print("First 3 ratings:")
            for i, rating in enumerate(user_ratings[:3]):
                print(f"{i+1}. {rating['movie_title']}: {rating['rating']} stars")
    except Exception as e:
        print(f"❌ Error retrieving user ratings: {e}")
        return False
    return True

def test_get_movie_recommendations():
    """Test generating movie recommendations for a user."""
    print("\nTesting movie recommendations...")
    try:
        # Try to get recommendations for user ID 1
        recommendations = get_movie_recommendations(1, n=5)
        print(f"✅ Successfully generated {len(recommendations)} recommendations for user 1")
        print("Recommendations:")
        for i, rec in enumerate(recommendations):
            print(f"{i+1}. {rec['movie_title']}: estimated {rec['est_rating']} stars")
    except Exception as e:
        print(f"❌ Error generating recommendations: {e}")
        return False
    return True

def main():
    """Run all tests."""
    print("=== TESTING DATA LOADER MODULE ===\n")
    
    tests = [
        test_check_data_files,
        test_load_movies,
        test_load_ratings,
        test_load_poster_links,
        test_get_movie_metadata,
        test_get_user_ratings,
        test_get_movie_recommendations
    ]
    
    success_count = 0
    for test in tests:
        if test():
            success_count += 1
    
    print(f"\n=== TEST RESULTS: {success_count}/{len(tests)} tests passed ===")

if __name__ == "__main__":
    main() 