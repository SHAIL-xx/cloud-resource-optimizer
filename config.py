import os
import boto3
from dotenv import load_dotenv

load_dotenv()

def get_ec2_client():
    use_local = os.getenv("USE_LOCAL_EMULATOR", "False").lower() == "true"
    endpoint = os.getenv("LOCALSTACK_ENDPOINT", "http://127.0.0.1:4566")
    region = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
    
    if use_local:
        return boto3.client('ec2', endpoint_url=endpoint, region_name=region)
    return boto3.client('ec2', region_name=region)