import logging
import os

from arctic import Arctic
from flask import Flask

from blueprints.example_endpoints import construct_example_endpoints

# Set up logging format
fmt = logging.Formatter(
          fmt='%(asctime)s [%(levelname)s] %(module)s: %(message)s',
          datefmt='%Y-%m-%dT%H:%M:%S%z')

# Set up logging to stream
fh = logging.StreamHandler()

# Get the root logger
logger = logging.getLogger()

# Set level and add handler
logger.setLevel(logging.INFO)
fh.setFormatter(fmt)
logger.addHandler(fh)

# Define Flask application
app = Flask(__name__)

# Initialzie MongoDB connection
mongo_host = f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}@{os.getenv('MONGO_CLUSTER')}.2tlis.mongodb.net/retryWrites=true&w=majority"
store = Arctic(mongo_host)

# Construct blueprints
example_endpoints = construct_example_endpoints(store)

# Register blueprints
app.register_blueprint(example_endpoints)

# Just a test endpoint
@app.route('/')
def index():
    return "This API is Alive"

# Run the flask app
if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')
