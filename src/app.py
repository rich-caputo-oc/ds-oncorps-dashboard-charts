import logging
import os

from arctic import Arctic
from flask import Flask

from blueprints.user_engagement_endpoints import construct_user_engagement_endpoints
from blueprints.data_endpoints import construct_data_endpoints

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
user_engagement_endpoints = construct_user_engagement_endpoints(store)
data_endpoints = construct_data_endpoints(store)

# Register blueprints
app.register_blueprint(user_engagement_endpoints)
app.register_blueprint(data_endpoints)

# Just a test endpoint
@app.route('/')
def index():
    return "This API is Alive"

@app.route('/all-endpoints')
def all_endpoints():
    return str([str(rule) for rule in app.url_map.iter_rules()])

# Run the flask app
if __name__ == '__main__':
    app.run(port=4000, host='0.0.0.0')
