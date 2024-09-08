import os
from dotenv import load_dotenv

def load_env_variables():
    load_dotenv()
    os.environ['CO_API_KEY'] = os.getenv('CO_API_KEY')