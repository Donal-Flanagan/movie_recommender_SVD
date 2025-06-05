import os
from dotenv import load_dotenv
# Load environment variables from both .env and .flaskenv files
# Make sure .flaskenv is loaded first so .env can override if needed
load_dotenv(".flaskenv")
load_dotenv()

from application import create_app

app = create_app()

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    app.run(debug=True, port=port)