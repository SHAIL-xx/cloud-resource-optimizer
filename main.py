import os
import argparse
import requests
from config import get_ec2_client
from scanner import find_unattached_volumes, find_unassociated_eips
from remediator import cleanup_resources

def generate_report(orphans, total_waste):
    print("\n" + "="*60)
    print(" ☁️  CLOUD RESOURCE OPTIMIZATION REPORT ☁️")
    print("="*60)
    
    if not orphans:
        print("\nNo idle resources found. Your environment is optimized!\n")
        print("="*60 + "\n")
        return

    print(f"{'RESOURCE ID':<25} | {'TYPE':<18} | {'WASTE/MO'}")
    print("-" * 60)
    
    for resource in orphans:
        cost = f"${resource['MonthlyWaste']:.2f}"
        print(f"{resource['ResourceId']:<25} | {resource['Type']:<18} | {cost}")
        
    print("-" * 60)
    print(f"{'TOTAL ESTIMATED MONTHLY SAVINGS:':<46} | ${total_waste:.2f}")
    print("="*60 + "\n")

def send_discord_alert(orphans, total_waste):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("[INFO] No DISCORD_WEBHOOK_URL found. Skipping Discord alert.")
        return

    if not orphans:
        color = 3066993  # Green
        description = "✅ No idle resources found. Your environment is optimized!"
    else:
        color = 15158332 # Red
        description = f"🚨 Found **{len(orphans)}** orphaned resources wasting **${total_waste:.2f}** per month."

    payload = {
        "username": "FinOps Bot",
        "embeds": [
            {
                "title": "☁️ Cloud Resource Optimization Report",
                "description": description,
                "color": color
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("✅ Successfully pushed report to Discord!")
    except Exception as e:
        print(f"❌ Failed to send Discord alert: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and delete orphaned AWS resources.")
    parser.add_argument('--execute', action='store_true', help="Actually delete the resources.")
    args = parser.parse_args()

    ec2_client = get_ec2_client()
    
    print("Scanning environment for orphaned resources...")
    all_orphans = find_unattached_volumes(ec2_client) + find_unassociated_eips(ec2_client)
    total_waste = sum(res['MonthlyWaste'] for res in all_orphans)
    
    generate_report(all_orphans, total_waste)
    send_discord_alert(all_orphans, total_waste)

    if all_orphans:
        cleanup_resources(ec2_client, all_orphans, dry_run=not args.execute)