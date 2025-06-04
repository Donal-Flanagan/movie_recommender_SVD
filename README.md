# Movie Recommender System

A web application that recommends movies based on user preferences using Singular Value Decomposition (SVD).

## Features

- User authentication and session management
- Movie catalog browsing with filtering and search
- Movie rating system
- Personalized movie recommendations
- Responsive and intuitive user interface

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 4
- **Backend**: Python, Flask
- **Database**: MongoDB
- **ML Library**: Surprise library for SVD implementation

## Project Structure

```
movie_recommender_SVD/
├── .cursor/             # Cursor IDE rules
├── .flaskenv            # Flask environment variables
├── main.py              # Application entry point
├── config.py            # Configuration settings
├── application/         # Main application package
│   ├── __init__.py      # Application factory
│   ├── routes.py        # Route definitions
│   ├── models.py        # Database models
│   ├── forms.py         # Form definitions
│   ├── static/          # Static files (CSS, JS, etc.)
│   └── templates/       # Jinja2 templates
├── models/              # Saved ML models
├── utils/               # Utility functions
└── docs/                # Documentation
    ├── overview/        # Project overview
    ├── backend/         # Backend documentation
    ├── frontend/        # Frontend documentation
    └── machine_learning/# ML documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/movie_recommender_SVD.git
   cd movie_recommender_SVD
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv flaskenv
   source flaskenv/bin/activate  # On Windows: flaskenv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up MongoDB:
   - Install MongoDB if not already installed
   - Create a database named `movie_recommender`

5. Configure environment variables:
   - Create a `.env` file in the project root
   - Add your MongoDB connection details and secret key

6. Initialize the database:
   ```
   python init_db.py
   ```

7. Run the application:
   ```
   flask run
   ```

## Usage

1. Open your browser and navigate to `http://localhost:8081`
2. Register or log in to your account
3. Browse the movie catalog and rate movies
4. View personalized recommendations based on your ratings

## Development

This project is developed incrementally, following these stages:

1. **Version 1**: Basic Flask application setup
2. **Version 2**: Frontend templates and static assets
3. **Version 3**: Data integration and template rendering
4. **Version 4**: MongoDB database integration
5. **Version 5**: User authentication and session management
6. **Version 6**: SVD model integration and personalized recommendations

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **Project Overview**: `docs/overview/project_overview.md`
- **Backend Documentation**: `docs/backend/backend_documentation.md`
- **Frontend Documentation**: `docs/frontend/frontend_documentation.md`
- **Machine Learning Documentation**: `docs/machine_learning/ml_documentation.md`

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Surprise](https://surpriselib.com/) - A Python scikit for recommender systems
- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [MongoDB](https://www.mongodb.com/) - The database platform
- [MovieLens](https://grouplens.org/datasets/movielens/) - Dataset for movie recommendations
- [Bootstrap](https://getbootstrap.com/) - Frontend component library 