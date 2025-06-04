# Frontend Documentation

## Overview

The frontend of the Movie Recommender System is built using HTML, CSS, and JavaScript, with Jinja2 as the templating engine. It provides a responsive and intuitive user interface for browsing movies, rating them, and viewing personalized recommendations.

## Directory Structure

```
application/
├── static/
│   ├── css/
│   │   ├── main.css             # Main stylesheet
│   │   ├── custom_style.css     # Custom styles
│   │   └── bootstrap.min.css    # Bootstrap framework
│   ├── js/
│   │   ├── main.js              # Main JavaScript file
│   │   ├── ratings.js           # Rating functionality
│   │   └── bootstrap.min.js     # Bootstrap JavaScript
│   └── img/
│       ├── favicon.ico          # Site favicon
│       └── logo.png             # Site logo
└── templates/
    ├── layout.html              # Base template
    ├── includes/
    │   ├── nav.html             # Navigation component
    │   └── footer.html          # Footer component
    ├── index.html               # Home page
    ├── catalog.html             # Movie catalog
    ├── login.html               # Login page
    ├── reviews.html             # User reviews
    ├── recommend.html           # Recommendations
    └── errors/
        ├── 404.html             # Not found error
        └── 500.html             # Server error
```

## Template Structure

### Base Layout

The `layout.html` file serves as the base template for all pages. It includes common elements like the head section, navigation bar, and footer.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Movie Recommender{% endblock %}</title>
    
    <!-- CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/custom_style.css') }}">
    
    <!-- Favicon -->
    <link rel="shortcut icon" href="{{ url_for('static', filename='img/favicon.ico') }}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation -->
    {% include "includes/nav.html" %}
    
    <!-- Flash Messages -->
    <div class="container mt-3">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show">
                        {{ message }}
                        <button type="button" class="close" data-dismiss="alert">&times;</button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>
    
    <!-- Main Content -->
    <main class="container mt-4">
        {% if session.user_name %}
            <p class="text-muted">Logged in as: {{ session.user_name }}</p>
        {% endif %}
        
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    {% include "includes/footer.html" %}
    
    <!-- JavaScript -->
    <script src="{{ url_for('static', filename='js/jquery.min.js') }}"></script>
    <script src="{{ url_for('static', filename='js/bootstrap.min.js') }}"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Navigation Component

The navigation bar is defined in `includes/nav.html` and included in the base layout.

```html
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{{ url_for('index') }}">Movie Recommender</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item {% if navhome %}active{% endif %}">
                    <a class="nav-link" href="{{ url_for('index') }}">Home</a>
                </li>
                <li class="nav-item {% if navcatalog %}active{% endif %}">
                    <a class="nav-link" href="{{ url_for('catalog') }}">Catalog</a>
                </li>
                {% if session.user_id %}
                    <li class="nav-item {% if navreviews %}active{% endif %}">
                        <a class="nav-link" href="{{ url_for('reviews') }}">My Reviews</a>
                    </li>
                    <li class="nav-item {% if navrecommend %}active{% endif %}">
                        <a class="nav-link" href="{{ url_for('recommend') }}">Recommendations</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                    </li>
                {% else %}
                    <li class="nav-item {% if navlogin %}active{% endif %}">
                        <a class="nav-link" href="{{ url_for('login') }}">Login</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
```

## Page Templates

### Home Page (index.html)

The home page provides an introduction to the movie recommender system.

```html
{% extends "layout.html" %}

{% block title %}Home - Movie Recommender{% endblock %}

{% block content %}
    <div class="jumbotron">
        <h1 class="display-4">Welcome to Movie Recommender</h1>
        <p class="lead">Discover new movies based on your personal preferences.</p>
        <hr class="my-4">
        <p>Rate movies you've watched, and we'll recommend movies you might enjoy!</p>
        {% if not session.user_id %}
            <a class="btn btn-primary btn-lg" href="{{ url_for('login') }}" role="button">Login to Get Started</a>
        {% else %}
            <a class="btn btn-primary btn-lg" href="{{ url_for('recommend') }}" role="button">View Recommendations</a>
        {% endif %}
    </div>
    
    <div class="row mt-5">
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Browse Movies</h5>
                    <p class="card-text">Explore our extensive catalog of movies.</p>
                    <a href="{{ url_for('catalog') }}" class="btn btn-outline-primary">Catalog</a>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Rate Movies</h5>
                    <p class="card-text">Share your opinions on movies you've watched.</p>
                    <a href="{{ url_for('reviews') }}" class="btn btn-outline-primary">My Reviews</a>
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Get Recommendations</h5>
                    <p class="card-text">Discover new movies based on your ratings.</p>
                    <a href="{{ url_for('recommend') }}" class="btn btn-outline-primary">Recommendations</a>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

### Movie Catalog (catalog.html)

The catalog page displays all movies in the database, with optional filtering and pagination.

```html
{% extends "layout.html" %}

{% block title %}Movie Catalog - Movie Recommender{% endblock %}

{% block content %}
    <h1>Movie Catalog</h1>
    
    <div class="row mb-4">
        <div class="col-md-6">
            <form method="GET" action="{{ url_for('catalog') }}">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search movies..." name="search" value="{{ request.args.get('search', '') }}">
                    <div class="input-group-append">
                        <button class="btn btn-outline-primary" type="submit">Search</button>
                    </div>
                </div>
            </form>
        </div>
        <div class="col-md-6">
            <div class="form-group">
                <select class="form-control" id="genre-filter">
                    <option value="">All Genres</option>
                    {% for genre in genres %}
                        <option value="{{ genre }}">{{ genre }}</option>
                    {% endfor %}
                </select>
            </div>
        </div>
    </div>
    
    <div class="row">
        {% for movie in movies %}
            <div class="col-md-4 mb-4 movie-card" data-genres="{{ movie.genres|join(',') }}">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">{{ movie.title }}</h5>
                        <p class="card-text"><small class="text-muted">{{ movie.release_date.strftime('%Y') if movie.release_date }}</small></p>
                        <p class="card-text">
                            {% for genre in movie.genres %}
                                <span class="badge badge-secondary">{{ genre }}</span>
                            {% endfor %}
                        </p>
                        {% if session.user_id %}
                            <div class="rating-container">
                                <p>Rate this movie:</p>
                                <div class="star-rating" data-movie-id="{{ movie.id }}">
                                    {% for i in range(1, 6) %}
                                        <i class="far fa-star" data-rating="{{ i }}"></i>
                                    {% endfor %}
                                </div>
                            </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
    
    <!-- Pagination -->
    <nav aria-label="Page navigation">
        <ul class="pagination justify-content-center">
            {% if pagination.has_prev %}
                <li class="page-item">
                    <a class="page-link" href="{{ url_for('catalog', page=pagination.prev_num) }}">Previous</a>
                </li>
            {% else %}
                <li class="page-item disabled">
                    <span class="page-link">Previous</span>
                </li>
            {% endif %}
            
            {% for page in pagination.iter_pages() %}
                {% if page %}
                    <li class="page-item {% if page == pagination.page %}active{% endif %}">
                        <a class="page-link" href="{{ url_for('catalog', page=page) }}">{{ page }}</a>
                    </li>
                {% else %}
                    <li class="page-item disabled">
                        <span class="page-link">...</span>
                    </li>
                {% endif %}
            {% endfor %}
            
            {% if pagination.has_next %}
                <li class="page-item">
                    <a class="page-link" href="{{ url_for('catalog', page=pagination.next_num) }}">Next</a>
                </li>
            {% else %}
                <li class="page-item disabled">
                    <span class="page-link">Next</span>
                </li>
            {% endif %}
        </ul>
    </nav>
{% endblock %}

{% block extra_js %}
    <script src="{{ url_for('static', filename='js/ratings.js') }}"></script>
    <script>
        // Genre filtering functionality
        document.getElementById('genre-filter').addEventListener('change', function() {
            const selectedGenre = this.value;
            const movieCards = document.querySelectorAll('.movie-card');
            
            movieCards.forEach(card => {
                const genres = card.dataset.genres.split(',');
                if (!selectedGenre || genres.includes(selectedGenre)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    </script>
{% endblock %}
```

### Login Page (login.html)

The login page provides a form for user authentication.

```html
{% extends "layout.html" %}

{% block title %}Login - Movie Recommender{% endblock %}

{% block content %}
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-center">Login</h3>
                </div>
                <div class="card-body">
                    <form method="POST" action="{{ url_for('login') }}">
                        {{ form.hidden_tag() }}
                        
                        <div class="form-group">
                            {{ form.email.label(class="form-control-label") }}
                            {% if form.email.errors %}
                                {{ form.email(class="form-control is-invalid") }}
                                <div class="invalid-feedback">
                                    {% for error in form.email.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% else %}
                                {{ form.email(class="form-control") }}
                            {% endif %}
                        </div>
                        
                        <div class="form-group">
                            {{ form.password.label(class="form-control-label") }}
                            {% if form.password.errors %}
                                {{ form.password(class="form-control is-invalid") }}
                                <div class="invalid-feedback">
                                    {% for error in form.password.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% else %}
                                {{ form.password(class="form-control") }}
                            {% endif %}
                        </div>
                        
                        <div class="form-group">
                            {{ form.submit(class="btn btn-primary btn-block") }}
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

## CSS Structure

### Main Stylesheet (main.css)

The main stylesheet provides global styles for the application.

```css
/* Global styles */
body {
    font-family: 'Arial', sans-serif;
    color: #333;
    background-color: #f8f9fa;
    margin-bottom: 60px; /* For fixed footer */
}

/* Footer */
footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    height: 60px;
    background-color: #343a40;
    color: white;
    display: flex;
    align-items: center;
}

/* Card styles */
.card {
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Rating stars */
.star-rating {
    color: #ffc107;
    cursor: pointer;
    font-size: 1.2rem;
}

.star-rating .fa-star,
.star-rating .fa-star-half-alt {
    margin-right: 5px;
}

/* Movie cards */
.movie-card {
    margin-bottom: 20px;
}

/* Genre badges */
.badge-secondary {
    margin-right: 5px;
    background-color: #6c757d;
}
```

## JavaScript Functionality

### Main JavaScript (main.js)

The main JavaScript file contains global functionality used across the application.

```javascript
// Enable Bootstrap tooltips
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
});

// Flash message auto-close
setTimeout(function() {
    $('.alert').alert('close');
}, 5000);

// Mobile menu toggle
$('.navbar-toggler').on('click', function() {
    $(this).toggleClass('active');
});

// Add smooth scrolling to all links
$('a').on('click', function(event) {
    if (this.hash !== '') {
        event.preventDefault();
        const hash = this.hash;
        $('html, body').animate({
            scrollTop: $(hash).offset().top
        }, 800, function(){
            window.location.hash = hash;
        });
    }
});
```

### Rating Functionality (ratings.js)

The ratings.js file handles movie rating functionality.

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Star rating functionality
    const starRatings = document.querySelectorAll('.star-rating');
    
    starRatings.forEach(container => {
        const stars = container.querySelectorAll('i');
        const movieId = container.dataset.movieId;
        
        // Set initial state if there's a saved rating
        if (container.dataset.userRating) {
            const userRating = parseInt(container.dataset.userRating);
            highlightStars(stars, userRating);
        }
        
        // Handle mouse hover
        stars.forEach(star => {
            star.addEventListener('mouseover', function() {
                const rating = parseInt(this.dataset.rating);
                highlightStars(stars, rating);
            });
            
            star.addEventListener('mouseout', function() {
                // Reset to current rating or clear if none
                if (container.dataset.userRating) {
                    const userRating = parseInt(container.dataset.userRating);
                    highlightStars(stars, userRating);
                } else {
                    clearStars(stars);
                }
            });
            
            // Handle click to set rating
            star.addEventListener('click', function() {
                const rating = parseInt(this.dataset.rating);
                submitRating(movieId, rating, container);
            });
        });
    });
    
    // Helper functions
    function highlightStars(stars, rating) {
        stars.forEach((star, index) => {
            if (index < rating) {
                star.classList.remove('far');
                star.classList.add('fas');
            } else {
                star.classList.remove('fas');
                star.classList.add('far');
            }
        });
    }
    
    function clearStars(stars) {
        stars.forEach(star => {
            star.classList.remove('fas');
            star.classList.add('far');
        });
    }
    
    function submitRating(movieId, rating, container) {
        fetch('/rate/' + movieId, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ rating: rating })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update UI to reflect the saved rating
                container.dataset.userRating = rating;
                showMessage('Rating saved!', 'success');
            } else {
                showMessage('Error saving rating. Please try again.', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Error saving rating. Please try again.', 'danger');
        });
    }
    
    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }
    
    function showMessage(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="close" data-dismiss="alert">&times;</button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 3000);
    }
});
```

## Responsive Design

The application is built with responsive design principles using Bootstrap 4's grid system and components. Key responsive features include:

1. **Fluid Containers**: The main content uses Bootstrap's container classes to adjust width based on screen size.

2. **Responsive Grid**: Content is organized using the 12-column grid system, with different column sizes for different screen sizes.

3. **Collapsible Navigation**: The navigation bar collapses into a hamburger menu on smaller screens.

4. **Flexible Images**: Images use `img-fluid` class to scale with their containers.

5. **Media Queries**: Custom CSS includes media queries to adjust specific elements for different screen sizes.

## Accessibility Considerations

The frontend implements several accessibility features:

1. **Semantic HTML**: Using appropriate semantic elements like `<nav>`, `<main>`, `<footer>`.

2. **ARIA Attributes**: Including roles and aria-labels where appropriate.

3. **Alt Text**: All images have descriptive alt text.

4. **Form Labels**: All form inputs have proper labels.

5. **Color Contrast**: Ensuring sufficient contrast between text and background colors.

6. **Keyboard Navigation**: All interactive elements are accessible via keyboard.

## Performance Optimization

Several techniques are used to optimize frontend performance:

1. **Minified Assets**: CSS and JavaScript files are minified for production.

2. **Lazy Loading**: Images below the fold are lazy-loaded.

3. **CSS Optimization**: CSS is placed in the head, and JavaScript is loaded at the end of the body.

4. **Caching**: Static assets are cached using appropriate cache headers.

5. **Compressed Images**: Images are compressed to reduce file size without sacrificing quality. 