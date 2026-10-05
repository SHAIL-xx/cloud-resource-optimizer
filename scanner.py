def find_unattached_volumes(client):
    response = client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    orphans = []
    for vol in response.get('Volumes', []):
        vol_type = vol['VolumeType']
        cost = 4.00 if vol_type == 'gp2' else 1.60
        orphans.append({
            'ResourceId': vol['VolumeId'],
            'Type': f'EBS Volume ({vol_type})',
            'MonthlyWaste': cost
        })
    return orphans

def find_unassociated_eips(client):
    response = client.describe_addresses()
    orphans = []
    for eip in response.get('Addresses', []):
        if 'AssociationId' not in eip:
            orphans.append({
                'ResourceId': eip.get('PublicIp', eip.get('AllocationId')),
                'Type': 'Elastic IP',
                'MonthlyWaste': 3.60
            })
    return orphans