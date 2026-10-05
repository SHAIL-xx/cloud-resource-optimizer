from botocore.exceptions import ClientError

def find_unattached_volumes(client):
    """Scans for EBS volumes that are provisioned but not attached to any EC2 instance."""
    wasted_resources = []
    
    try:
        # The 'available' state means it exists but is not in use
        response = client.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )
        
        for vol in response.get('Volumes', []):
            size_gb = vol['Size']
            # Using a generic $0.08/GB monthly cost estimate for gp3 volumes
            estimated_cost = round(size_gb * 0.08, 2)
            
            wasted_resources.append({
                'ResourceId': vol['VolumeId'],
                'Type': f"EBS Volume ({vol['VolumeType']})",
                'SizeGB': size_gb,
                'MonthlyWaste': estimated_cost
            })
            
    except ClientError as e:
        print(f"[ERROR] Failed querying EBS volumes: {e}")
        
    return wasted_resources


def find_unassociated_eips(client):
    
    """Scans for Elastic IPs that are allocated to the account but not attached to a resource."""
    wasted_resources = []
    
    try:
        response = client.describe_addresses()
        
        for eip in response.get('Addresses', []):
            # An EIP without an AssociationId is sitting idle and costing money
            if 'AssociationId' not in eip:
                wasted_resources.append({
                    'ResourceId': eip.get('PublicIp', 'Unknown-IP'),
                    'AllocationId': eip.get('AllocationId'),
                    'Type': 'Elastic IP',
                    'MonthlyWaste': 3.60  # Approx $3.60/month for an idle IP
                })
                
    except ClientError as e:
        print(f"[ERROR] Failed querying Elastic IPs: {e}")
        
    return wasted_resources