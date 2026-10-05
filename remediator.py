def cleanup_resources(client, orphans, dry_run=True):
    print("\n" + "="*60)
    if dry_run:
        print(" DRY RUN MODE: No resources will be deleted  ")
    else:
        print(" DELETING RESOURCES ")
    print("="*60)
    
    for res in orphans:
        if dry_run:
            print(f"[DRY RUN] Would delete {res['Type']}: {res['ResourceId']}")
        else:
            try:
                if 'EBS Volume' in res['Type']:
                    client.delete_volume(VolumeId=res['ResourceId'])
                elif 'Elastic IP' in res['Type']:
                    if res['ResourceId'].startswith('eipalloc-'):
                        client.release_address(AllocationId=res['ResourceId'])
                    else:
                        client.release_address(PublicIp=res['ResourceId'])
                print(f"✅ Deleted {res['Type']}: {res['ResourceId']}")
            except Exception as e:
                print(f"❌ Failed to delete {res['ResourceId']}: {e}")
    print("="*60 + "\n")