// Main JavaScript for Movie Recommender

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
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
}); 