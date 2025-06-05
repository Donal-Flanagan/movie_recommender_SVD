// Main JavaScript for Movie Recommender

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide flash messages after 5 seconds
    var flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            var alert = bootstrap.Alert.getInstance(message);
            if (alert) {
                alert.close();
            } else {
                message.classList.add('fade');
                setTimeout(function() {
                    message.remove();
                }, 150);
            }
        }, 5000);
    });

    // Handle movie card interactions
    const movieCards = document.querySelectorAll('.card');
    movieCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('shadow');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('shadow');
        });
    });

    // Handle genre filter changes
    const genreFilter = document.querySelector('select[aria-label="Filter by genre"]');
    if (genreFilter) {
        genreFilter.addEventListener('change', function() {
            // In a real application, this would filter the movies
            console.log('Filter changed to:', this.value);
            // Placeholder for AJAX request or page reload with filter
        });
    }

    // Simple rating system
    const ratingButtons = document.querySelectorAll('.btn-outline-primary');
    ratingButtons.forEach(button => {
        if (button.textContent.trim() === 'Rate') {
            button.addEventListener('click', function() {
                // In a real application, this would open a rating modal
                const movieTitle = this.closest('.card').querySelector('.card-title').textContent;
                alert(`Rate "${movieTitle}"`);
                // Placeholder for rating functionality
            });
        }
    });

    // Add animation to newly loaded content
    function addFadeInAnimation() {
        const newContent = document.querySelector('.fade-in-trigger');
        if (newContent) {
            newContent.classList.add('fade-in');
            newContent.classList.remove('fade-in-trigger');
        }
    }
    
    // Call once on page load
    addFadeInAnimation();
});

// Utility functions
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
} 