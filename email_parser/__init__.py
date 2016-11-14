import os
from settings import google_api_credentials

project_dir = os.path.dirname(__file__)

google_api_credentials_file = os.path.join(project_dir, google_api_credentials)
