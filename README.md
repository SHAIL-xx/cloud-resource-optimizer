# Automated Cloud Resource Optimizer (FinOps)

An automated FinOps utility built with Python and Boto3 that audits AWS environments for orphaned, cost-incurring resources. It identifies idle assets, calculates monthly financial waste, and provides a strict dry-run remediation engine for safe deletion.

## Key Features

* **Cost-Aware Auditing:** Scans for unattached EBS volumes (`available` state) and unassociated Elastic IPs.
* **Financial Reporting:** Dynamically calculates estimated monthly cost savings and generates a clean console report.
* **Local Emulation:** Integrates with LocalStack via `.env` configuration to safely develop and test Boto3 API calls entirely offline.
* **Safe Remediation Engine:** Includes a strict `--execute` flag. By default, the script runs in read-only (Dry Run) mode to prevent accidental data loss.
* **Automated CI/CD Pipeline:** Uses GitHub Actions with a cron schedule to perform a weekly cost audit every Monday.

## Tech Stack

* **Language:** Python 3.12
* **Cloud SDK:** Boto3 (AWS SDK for Python)
* **Emulation:** LocalStack, Docker
* **Automation:** GitHub Actions

## Local Setup & Testing

**1. Install Dependencies**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt