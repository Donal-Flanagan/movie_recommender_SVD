# Machine Learning Documentation

## Overview

The Movie Recommender System employs Singular Value Decomposition (SVD) as its core recommendation algorithm. SVD is a matrix factorization technique used in collaborative filtering, which identifies latent factors that explain observed rating patterns.

## Recommendation Approach

### Collaborative Filtering

The system uses collaborative filtering, which makes recommendations based on the similarity patterns among users and items. Specifically, we implement model-based collaborative filtering using SVD, which:

1. Analyzes past user behavior (movie ratings)
2. Identifies patterns in user preferences
3. Predicts ratings for movies that users haven't seen yet
4. Recommends movies with the highest predicted ratings

### SVD Algorithm

SVD decomposes the user-item rating matrix into three matrices:

```
R ≈ U × Σ × V^T
```

Where:
- R is the original user-item rating matrix
- U is the user feature matrix
- Σ is a diagonal matrix of singular values
- V^T is the transposed item feature matrix

This decomposition allows us to represent users and movies in a lower-dimensional "latent factor" space, capturing the underlying features that influence user preferences.

## Implementation

### Surprise Library

The SVD implementation uses the Surprise library, a Python scikit for recommender systems:

```python
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split, cross_validate

# Configure the reader with rating scale
reader = Reader(rating_scale=(0.5, 5))

# Load the data
data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)

# Split the data into train and test sets
trainset, testset = train_test_split(data, test_size=0.2)

# Define the SVD algorithm with hyperparameters
algo = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.02)

# Train the model
algo.fit(trainset)

# Make predictions on the test set
predictions = algo.test(testset)
```

### Data Preprocessing

Before training the SVD model, the following preprocessing steps are applied:

1. **Data Loading**: Loading ratings data from MongoDB into a pandas DataFrame
2. **Data Cleaning**: Removing duplicate ratings, handling missing values
3. **Data Transformation**: Converting ratings to the appropriate numerical format
4. **Data Splitting**: Dividing data into training and testing sets

```python
def preprocess_ratings(ratings_collection):
    # Load ratings from MongoDB
    ratings_data = list(ratings_collection.find())
    
    # Convert to pandas DataFrame
    ratings_df = pd.DataFrame(ratings_data)
    
    # Clean data
    ratings_df = ratings_df.dropna(subset=['user', 'movie', 'rating'])
    ratings_df = ratings_df.drop_duplicates(subset=['user', 'movie'])
    
    # Map MongoDB ObjectIds to integer IDs for Surprise
    user_mapping = {uid: i for i, uid in enumerate(ratings_df['user'].unique())}
    movie_mapping = {mid: i for i, mid in enumerate(ratings_df['movie'].unique())}
    
    ratings_df['userId'] = ratings_df['user'].map(user_mapping)
    ratings_df['movieId'] = ratings_df['movie'].map(movie_mapping)
    
    return ratings_df, user_mapping, movie_mapping
```

### Model Training

The SVD model is trained using the following approach:

1. **Hyperparameter Tuning**: Grid search for optimal parameters
2. **Cross-Validation**: K-fold cross-validation to evaluate model performance
3. **Model Persistence**: Saving the trained model for later use

```python
def train_svd_model(ratings_df):
    # Create a dataset
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(ratings_df[['userId', 'movieId', 'rating']], reader)
    
    # Perform grid search to find optimal hyperparameters
    param_grid = {
        'n_factors': [50, 100, 150],
        'n_epochs': [20, 30],
        'lr_all': [0.002, 0.005, 0.01],
        'reg_all': [0.02, 0.05, 0.1]
    }
    
    gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
    gs.fit(data)
    
    # Get the best parameters
    best_params = gs.best_params['rmse']
    
    # Train the model with the best parameters
    algo = SVD(**best_params)
    trainset = data.build_full_trainset()
    algo.fit(trainset)
    
    return algo, best_params
```

### Model Evaluation

The model is evaluated using these metrics:

1. **RMSE (Root Mean Square Error)**: Measures the square root of the average squared difference between predicted and actual ratings
2. **MAE (Mean Absolute Error)**: Measures the average absolute difference between predicted and actual ratings
3. **Precision and Recall**: Measures how relevant the recommendations are

```python
def evaluate_model(algo, testset):
    # Make predictions on the test set
    predictions = algo.test(testset)
    
    # Calculate RMSE and MAE
    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)
    
    # Calculate precision and recall at k
    precisions, recalls = precision_recall_at_k(predictions, k=10, threshold=3.5)
    
    # Average precision and recall
    avg_precision = sum(prec for prec in precisions.values()) / len(precisions)
    avg_recall = sum(rec for rec in recalls.values()) / len(recalls)
    
    return {
        'rmse': rmse,
        'mae': mae,
        'precision': avg_precision,
        'recall': avg_recall
    }
```

### Model Persistence

The trained model is saved to disk using pickle for later use in the web application:

```python
def save_model(algo, filename, metadata=None):
    # Create model directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Save the model with metadata
    model_data = {
        'algorithm': algo,
        'timestamp': datetime.now().isoformat(),
        'metadata': metadata
    }
    
    with open(filename, 'wb') as f:
        pickle.dump(model_data, f)
```

## Recommendation Generation

### Prediction Pipeline

The recommendation pipeline follows these steps:

1. **Load Model**: Load the pre-trained SVD model
2. **Get User Profile**: Retrieve the user's existing ratings
3. **Generate Candidates**: Identify movies the user hasn't rated
4. **Predict Ratings**: Use the SVD model to predict ratings for candidate movies
5. **Rank Recommendations**: Sort movies by predicted rating and return the top N

```python
def generate_recommendations(user_id, n=10):
    # Load the model
    with open('models/svd_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
        algo = model_data['algorithm']
    
    # Get the user's ratings
    user_ratings = Rating.objects(user=user_id)
    rated_movie_ids = [r.movie.id for r in user_ratings]
    
    # Get candidate movies (movies the user hasn't rated)
    candidate_movies = Movie.objects(id__nin=rated_movie_ids)
    
    # Map MongoDB IDs to the IDs used in the SVD model
    user_mapping = model_data['metadata']['user_mapping']
    movie_mapping = model_data['metadata']['movie_mapping']
    
    # Get mapped user ID
    mapped_user_id = user_mapping.get(str(user_id))
    if mapped_user_id is None:
        # Handle cold start for new users
        return get_popular_movies(n)
    
    # Generate predictions for all candidate movies
    predictions = []
    for movie in candidate_movies:
        mapped_movie_id = movie_mapping.get(str(movie.id))
        if mapped_movie_id is not None:
            pred = algo.predict(mapped_user_id, mapped_movie_id)
            predictions.append((movie, pred.est))
    
    # Sort by predicted rating and return top N
    recommendations = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    
    return [movie for movie, _ in recommendations]
```

### Cold Start Problem

For new users with few or no ratings, the system employs a hybrid approach:

1. **Popular Items**: Recommend generally popular movies
2. **Content-Based Filtering**: Use movie metadata (genres, actors, directors) to make initial recommendations
3. **Interactive Learning**: Prompt users to rate a selection of diverse movies to establish preferences

```python
def get_popular_movies(n=10):
    # Find movies with the most ratings
    pipeline = [
        {'$group': {
            '_id': '$movie',
            'count': {'$sum': 1},
            'avg_rating': {'$avg': '$rating'}
        }},
        {'$match': {'count': {'$gt': 10}}},  # At least 10 ratings
        {'$sort': {'avg_rating': -1, 'count': -1}},
        {'$limit': n}
    ]
    
    popular_movies = list(Rating.objects.aggregate(pipeline))
    movie_ids = [doc['_id'] for doc in popular_movies]
    
    return Movie.objects(id__in=movie_ids)
```

## Integration with Flask

### Recommendation Service

The machine learning component is integrated with the Flask application through a service layer:

```python
# application/services/recommendation_service.py
import pickle
from application.models import User, Movie, Rating, Prediction
from surprise import SVD

class RecommendationService:
    def __init__(self, model_path='models/svd_model.pkl'):
        # Load the model on initialization
        with open(model_path, 'rb') as f:
            self.model_data = pickle.load(f)
            self.algo = self.model_data['algorithm']
            self.user_mapping = self.model_data['metadata']['user_mapping']
            self.movie_mapping = self.model_data['metadata']['movie_mapping']
            self.inv_user_mapping = {v: k for k, v in self.user_mapping.items()}
            self.inv_movie_mapping = {v: k for k, v in self.movie_mapping.items()}
    
    def get_recommendations(self, user_id, n=10):
        """Generate n movie recommendations for a user."""
        # Implementation as described above
        pass
    
    def update_user_predictions(self, user_id):
        """Update all predictions for a user in the database."""
        # Get the user's mapped ID
        mapped_user_id = self.user_mapping.get(str(user_id))
        if mapped_user_id is None:
            return False
        
        # Get movies the user hasn't rated
        user_ratings = Rating.objects(user=user_id)
        rated_movie_ids = [r.movie.id for r in user_ratings]
        candidate_movies = Movie.objects(id__nin=rated_movie_ids)
        
        # Clear existing predictions
        Prediction.objects(user=user_id).delete()
        
        # Generate and store new predictions
        for movie in candidate_movies:
            mapped_movie_id = self.movie_mapping.get(str(movie.id))
            if mapped_movie_id is not None:
                pred = self.algo.predict(mapped_user_id, mapped_movie_id)
                
                # Save prediction to database
                prediction = Prediction(
                    user=user_id,
                    movie=movie.id,
                    predicted_rating=pred.est
                )
                prediction.save()
        
        return True
```

### API Endpoints

The Flask application provides API endpoints to access the recommendation functionality:

```python
# application/routes.py
from application.services.recommendation_service import RecommendationService

# Initialize recommendation service
recommendation_service = RecommendationService()

@app.route('/recommend')
def recommend():
    if 'user_id' not in session:
        flash('Please log in to see recommendations', 'warning')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Get recommendations from service
    recommendations = recommendation_service.get_recommendations(user_id, n=10)
    
    return render_template('recommend.html', recommendations=recommendations, navrecommend=True)
```

## Periodic Model Updates

To keep recommendations fresh and accurate, the model is periodically retrained:

1. **Scheduled Updates**: The model is retrained on a schedule (e.g., weekly)
2. **Incremental Learning**: New ratings are incorporated into the model
3. **A/B Testing**: Different model versions are evaluated to ensure improvement

```python
def schedule_model_update():
    """Schedule regular model updates."""
    # This function would be called by a scheduler like APScheduler
    
    # Get all ratings
    ratings_df, user_mapping, movie_mapping = preprocess_ratings(Rating.objects)
    
    # Train new model
    algo, best_params = train_svd_model(ratings_df)
    
    # Save model with mappings
    save_model(
        algo, 
        'models/svd_model_' + datetime.now().strftime('%Y%m%d') + '.pkl',
        metadata={
            'user_mapping': user_mapping,
            'movie_mapping': movie_mapping,
            'hyperparameters': best_params
        }
    )
    
    # Also save as the current model
    save_model(
        algo, 
        'models/svd_model.pkl',
        metadata={
            'user_mapping': user_mapping,
            'movie_mapping': movie_mapping,
            'hyperparameters': best_params
        }
    )
```

## Potential Enhancements

Future improvements to the recommendation system could include:

1. **Hybrid Approaches**: Combining collaborative filtering with content-based methods
2. **Deep Learning Models**: Implementing neural network-based recommendation models
3. **Real-time Updates**: Updating recommendations immediately after new ratings
4. **Contextual Recommendations**: Considering time, location, and other contextual factors
5. **Diversity and Serendipity**: Ensuring recommendations aren't too similar and include surprising items
6. **Explainable AI**: Providing reasons for recommendations to improve user trust 