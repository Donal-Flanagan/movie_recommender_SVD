# Movie Recommender SVD

A movie recommendation system built with Flask and SVD (Singular Value Decomposition).

## Overview

This project implements a web-based movie recommendation system using the Netflix Prize dataset and the MovieLens dataset. It uses Singular Value Decomposition (SVD) to generate personalized movie recommendations for users based on their rating history.

## Features

- User authentication and session management
- Movie catalog with search and filtering
- User rating system
- Personalized movie recommendations using SVD
- Mobile-friendly responsive design

## Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB (optional, for database storage)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/movie_recommender_SVD.git
   cd movie_recommender_SVD
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv flaskenv
   source flaskenv/bin/activate  # On Windows: flaskenv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Extract the data files:
   ```
   python scripts/setup_data.py
   ```

5. Run the application:
   ```
   flask run
   ```

6. Open your browser and navigate to `http://localhost:5000`

## Data Sources

This project uses the following datasets:

- [MovieLens Small Dataset](https://grouplens.org/datasets/movielens/latest/) - Contains movie ratings and metadata
- TMDB Metadata - Contains additional movie information like posters and cast/crew details

The datasets are included as ZIP files in the repository and are extracted during setup.

## Project Structure

- `application/` - Main application package
  - `__init__.py` - Application factory
  - `routes.py` - Route definitions
  - `models.py` - Database models
  - `data_loader.py` - Data loading utilities
  - `templates/` - HTML templates
  - `static/` - Static assets (CSS, JS, images)
- `data/` - Data directory (contains ZIP files)
- `scripts/` - Utility scripts
- `models/` - ML model storage

## Development

### Running Tests

```
pytest
```

### Code Style

This project follows PEP 8 guidelines for Python code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [MovieLens](https://grouplens.org/datasets/movielens/) for providing the dataset
- [Netflix Prize](https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data) for the original competition dataset
- [Surprise](https://surprise.readthedocs.io/) library for SVD implementation 