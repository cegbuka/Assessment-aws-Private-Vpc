from dotenv import load_dotenv
import os

def get_aws_keys():
    load_dotenv()
    return os.getenv('AWS_ACCESS_KEY'), os.getenv('AWS_SECRET_KEY'), os.getenv('AWS_REGION')
