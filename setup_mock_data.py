from config import get_ec2_client
from botocore.exceptions import ClientError

def create_mock_resources():
    ec2 = get_ec2_client()
    
    try:
        print("Creating mock unattached EBS volumes...")
        # Create a 20GB gp3 volume
        ec2.create_volume(
            AvailabilityZone='ap-south-1a',
            Size=20,
            VolumeType='gp3'
        )
        # Create a 50GB gp2 volume
        ec2.create_volume(
            AvailabilityZone='ap-south-1b',
            Size=50,
            VolumeType='gp2'
        )
        
        print("Creating mock unassociated Elastic IPs...")
        # Allocate 2 separate Elastic IPs
        ec2.allocate_address(Domain='vpc')
        ec2.allocate_address(Domain='vpc')
        
        print("✅ Mock data provisioned successfully in LocalStack!")
        
    except ClientError as e:
        print(f"[ERROR] Failed to create mock data: {e}")
        print("Is LocalStack running?")

if __name__ == "__main__":
    create_mock_resources()