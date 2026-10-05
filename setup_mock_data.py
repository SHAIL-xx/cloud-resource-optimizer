from config import get_ec2_client

def create_mock_resources():
    print("[INFO] Connecting to Localstack emulator")
    ec2 = get_ec2_client()
    
    print("Creating mock unattached EBS volumes...")
    ec2.create_volume(AvailabilityZone='ap-south-1a', Size=10, VolumeType='gp3')
    ec2.create_volume(AvailabilityZone='ap-south-1a', Size=40, VolumeType='gp2')
    
    print("Creating mock unassociated Elastic IPs...")
    ec2.allocate_address(Domain='vpc')
    ec2.allocate_address(Domain='vpc')
    
    print(" Mock data provisioned successfully in LocalStack!")

if __name__ == "__main__":
    create_mock_resources()