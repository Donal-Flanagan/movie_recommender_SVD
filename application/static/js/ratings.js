/**
 * Ratings JavaScript for Movie Recommender
 * Handles star rating interactions and submissions
 */

class StarRating {
    constructor(container, options = {}) {
        this.container = container;
        this.options = Object.assign({
            maxRating: 5,
            initialRating: 0,
            readOnly: false,
            starSize: 'fs-5',
            onRate: null
        }, options);
        
        this.currentRating = this.options.initialRating;
        this.init();
    }
    
    init() {
        // Clear container
        this.container.innerHTML = '';
        this.container.classList.add('star-rating');
        
        // Create stars
        for (let i = 1; i <= this.options.maxRating; i++) {
            const star = document.createElement('i');
            star.classList.add('bi');
            star.classList.add(this.options.starSize);
            
            this.updateStarClass(star, i);
            
            if (!this.options.readOnly) {
                // Add hover effect
                star.addEventListener('mouseenter', () => this.hoverStar(i));
                star.addEventListener('mouseleave', () => this.resetStars());
                
                // Add click handler
                star.addEventListener('click', () => this.setRating(i));
            }
            
            this.container.appendChild(star);
        }
        
        // Add rating display if needed
        if (this.options.showRating) {
            const ratingText = document.createElement('span');
            ratingText.classList.add('ms-2');
            ratingText.textContent = this.currentRating > 0 ? `${this.currentRating}/${this.options.maxRating}` : '';
            this.ratingText = ratingText;
            this.container.appendChild(ratingText);
        }
    }
    
    updateStarClass(star, position) {
        star.classList.remove('bi-star', 'bi-star-fill', 'bi-star-half');
        
        if (position <= this.currentRating) {
            // Full star for integer ratings
            if (position <= Math.floor(this.currentRating)) {
                star.classList.add('bi-star-fill');
            } 
            // Half star for .5 ratings
            else if (position === Math.ceil(this.currentRating) && 
                     this.currentRating % 1 === 0.5) {
                star.classList.add('bi-star-half');
            } 
            // Empty star for positions greater than rating
            else {
                star.classList.add('bi-star');
            }
        } else {
            star.classList.add('bi-star');
        }
    }
    
    hoverStar(rating) {
        const stars = this.container.querySelectorAll('i');
        stars.forEach((star, index) => {
            star.classList.remove('bi-star', 'bi-star-fill', 'bi-star-half');
            if (index < rating) {
                star.classList.add('bi-star-fill');
            } else {
                star.classList.add('bi-star');
            }
        });
    }
    
    resetStars() {
        const stars = this.container.querySelectorAll('i');
        stars.forEach((star, index) => {
            this.updateStarClass(star, index + 1);
        });
    }
    
    setRating(rating) {
        this.currentRating = rating;
        this.resetStars();
        
        if (this.options.showRating && this.ratingText) {
            this.ratingText.textContent = `${this.currentRating}/${this.options.maxRating}`;
        }
        
        if (typeof this.options.onRate === 'function') {
            this.options.onRate(this.currentRating);
        }
    }
    
    getRating() {
        return this.currentRating;
    }
}

// Initialize all rating containers when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize static ratings (read-only)
    const staticRatingContainers = document.querySelectorAll('.static-rating');
    staticRatingContainers.forEach(container => {
        const rating = parseFloat(container.dataset.rating) || 0;
        new StarRating(container, {
            initialRating: rating,
            readOnly: true,
            showRating: true
        });
    });
    
    // Initialize interactive ratings
    const interactiveRatingContainers = document.querySelectorAll('.interactive-rating');
    interactiveRatingContainers.forEach(container => {
        const movieId = container.dataset.movieId;
        
        new StarRating(container, {
            initialRating: parseFloat(container.dataset.userRating) || 0,
            showRating: true,
            onRate: (rating) => {
                // In a real app, this would submit the rating to the server
                console.log(`Rated movie ${movieId} with ${rating} stars`);
                
                // Placeholder for AJAX submission
                const ratingStatus = container.parentElement.querySelector('.rating-status');
                if (ratingStatus) {
                    ratingStatus.textContent = 'Rating saved!';
                    ratingStatus.classList.add('text-success');
                    
                    // Clear the message after 3 seconds
                    setTimeout(() => {
                        ratingStatus.textContent = '';
                    }, 3000);
                }
            }
        });
    });
}); 