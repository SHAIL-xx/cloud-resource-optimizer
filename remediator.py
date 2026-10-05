from botocore.exceptions import ClientError

def cleanup_resources(client, resources, dry_run=True):
    print("\n" + "="*60)
    if dry_run:
        print(" DRY RUN MODE: No resources will be deleted  ")
    else:
        print("  EXECUTION MODE: Deleting resources...  ")
    print("="*60)

    for res in resources:
        res_id = res['ResourceId']
        res_type = res['Type']

        if dry_run:
            print(f"[DRY RUN] Would delete {res_type}: {res_id}")
            continue

        try:
            if 'EBS Volume' in res_type:
                client.delete_volume(VolumeId=res_id)
                print(f" Deleted {res_type}: {res_id}")
            
            elif 'Elastic IP' in res_type:
                allocation_id = res.get('AllocationId')
                if allocation_id:
                    client.release_address(AllocationId=allocation_id)
                    print(f" Released {res_type}: {res_id}")
                else:
                    print(f" Missing AllocationId for {res_id}")

        except ClientError as e:
            print(f"  Failed to delete {res_id}: {e}")
    
    print("="*60 + "\n")