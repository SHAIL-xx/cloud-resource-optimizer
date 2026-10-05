import argparse
from config import get_ec2_client
from scanner import find_unattached_volumes, find_unassociated_eips
from remediator import cleanup_resources

def generate_report(orphans):
    # ... (Keep your existing generate_report function exactly the same) ...
    print("\n" + "="*60)
    print(" ☁️  CLOUD RESOURCE OPTIMIZATION REPORT ☁️")
    print("="*60)
    
    if not orphans:
        print("\nNo idle resources found. Your environment is optimized!\n")
        print("="*60 + "\n")
        return

    total_waste = 0
    print(f"{'RESOURCE ID':<25} | {'TYPE':<18} | {'WASTE/MO'}")
    print("-" * 60)
    
    for resource in orphans:
        cost = f"${resource['MonthlyWaste']:.2f}"
        print(f"{resource['ResourceId']:<25} | {resource['Type']:<18} | {cost}")
        total_waste += resource['MonthlyWaste']
        
    print("-" * 60)
    print(f"{'TOTAL ESTIMATED MONTHLY SAVINGS:':<46} | ${total_waste:.2f}")
    print("="*60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and delete orphaned AWS resources.")
    parser.add_argument('--execute', action='store_true', help="Actually delete the resources.")
    args = parser.parse_args()

    ec2_client = get_ec2_client()
    
    print("Scanning environment for orphaned resources...")
    all_orphans = find_unattached_volumes(ec2_client) + find_unassociated_eips(ec2_client)
    
    generate_report(all_orphans)

    if all_orphans:
        # If --execute is passed, args.execute is True, so dry_run becomes False
        cleanup_resources(ec2_client, all_orphans, dry_run=not args.execute)