import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_ec2_client():
    # Initializes te EC2 Client,routing to Localstack if configured"
    use_emulator = os.getenv('USE_LOCAL_EMULATOR', 'False').lower() == 'true'
    
    if use_emulator:
        print("[INFO] Connecting to Localstack emulator")
        return boto3.client(
            'ec2',
            endpoint_url=os.getenv('LOCALSTACK_ENDPOINT','http://localhost:4566'),
            region_name=os.getenv('AWS_DEFAULT_REGION','ap-south-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID','test'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY','test')
        )

    
    # Connects to real AWS using your ~/.aws/credentials profile
    print("[INFO] Connecting to real AWS environment...")
    return boto3.client('ec2', region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))
 