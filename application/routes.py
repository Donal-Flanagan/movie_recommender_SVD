from flask import Blueprint, render_template, redirect, url_for
from datetime import datetime, UTC

# Create a Blueprint for the main routes
main = Blueprint('main', __name__)

@main.context_processor
def inject_now():
    """Add current year to all templates."""
    return {'now': datetime.now(UTC)}

@main.route('/')
def index():
    """Homepage route"""
    return render_template('index.html', title='Home')
