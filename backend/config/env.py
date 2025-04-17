from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
if not mongo_uri:
    raise ValueError("MONGODB_URI not set in environment variables.")
