"""
Sync categorized benefits data from JSON files to Supabase
This script reads the categorized data from backend/categorized_data/ 
and syncs it to the Supabase database.
"""

import os
import json
import sys
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    print("Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

CATEGORIZED_DIR = "categorized_data"


def get_latest_categorized_file() -> str:
    """Get the most recently created categorized JSON file"""
    if not os.path.exists(CATEGORIZED_DIR):
        print(f"Error: Directory {CATEGORIZED_DIR} does not exist")
        sys.exit(1)
    
    json_files = [
        f for f in os.listdir(CATEGORIZED_DIR) 
        if f.endswith('_categorized.json') or f.endswith('_categorized_*.json')
    ]
    
    if not json_files:
        print(f"Error: No categorized JSON files found in {CATEGORIZED_DIR}")
        sys.exit(1)
    
    # Sort by modification time, most recent first
    json_files.sort(key=lambda x: os.path.getmtime(os.path.join(CATEGORIZED_DIR, x)), reverse=True)
    
    latest_file = os.path.join(CATEGORIZED_DIR, json_files[0])
    print(f"Using latest categorized file: {latest_file}")
    return latest_file


def load_categorized_data(file_path: str) -> Dict[str, Any]:
    """Load and parse the categorized JSON data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully loaded data from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading JSON file: {str(e)}")
        sys.exit(1)


def clear_existing_benefits():
    """Clear all existing benefits from the database"""
    try:
        # Delete all existing benefits
        response = supabase.table('benefits').delete().neq('id', 0).execute()
        print(f"Cleared existing benefits from database")
    except Exception as e:
        print(f"Error clearing existing benefits: {str(e)}")


def format_plan_description(plan: Dict[str, Any]) -> str:
    """Format a plan's details into a readable description"""
    description_parts = []
    
    # Add key features
    if 'Key Features/Benefits' in plan and plan['Key Features/Benefits']:
        features = plan['Key Features/Benefits']
        if isinstance(features, list):
            description_parts.append("Features: " + "; ".join(features[:3]))  # Limit to 3 features
        else:
            description_parts.append(f"Features: {features}")
    
    # Add coverage details if available
    if 'Coverage Details' in plan and plan['Coverage Details']:
        description_parts.append(f"Coverage: {plan['Coverage Details']}")
    
    # Add eligibility if available
    if 'Eligibility Requirements' in plan and plan['Eligibility Requirements']:
        eligibility = plan['Eligibility Requirements']
        if eligibility != "Not mentioned." and eligibility != "Not mentioned":
            description_parts.append(f"Eligibility: {eligibility}")
    
    return " | ".join(description_parts) if description_parts else "No description available"


def extract_cost_info(plan: Dict[str, Any]) -> str:
    """Extract cost information from a plan"""
    cost_info = plan.get('Cost Information', '')
    if cost_info and cost_info != "Not mentioned." and cost_info != "Not mentioned":
        return cost_info
    return "Contact HR for pricing details"


def sync_benefits_to_supabase(categorized_data: Dict[str, Any]):
    """Sync benefits data to Supabase"""
    categories = categorized_data.get('categories', {})
    
    # Mapping of category names to readable benefit types
    category_mapping = {
        'health_insurance': 'Health Insurance',
        'dental_insurance': 'Dental Insurance',
        'vision_insurance': 'Vision Insurance',
        'life_insurance': 'Life Insurance',
        'disability_insurance': 'Disability Insurance',
        'employee_assistance': 'Employee Assistance Program',
        'retirement_plans': 'Retirement Plans',
        'other_benefits': 'Supplemental Benefits'
    }
    
    benefits_to_insert = []
    
    for category_key, category_name in category_mapping.items():
        plans = categories.get(category_key, [])
        
        if not plans:
            print(f"No plans found for category: {category_name}")
            continue
        
        print(f"\nProcessing {len(plans)} plans in category: {category_name}")
        
        for plan in plans:
            plan_name = plan.get('Plan Name', 'Unknown Plan')
            
            # Create benefit record
            benefit = {
                'name': plan_name,
                'description': format_plan_description(plan),
                'cost': extract_cost_info(plan),
                'category': category_name,
                'created_at': datetime.now().isoformat()
            }
            
            benefits_to_insert.append(benefit)
            print(f"  - Prepared: {plan_name}")
    
    # Insert benefits in batch
    if benefits_to_insert:
        try:
            print(f"\nInserting {len(benefits_to_insert)} benefits into Supabase...")
            response = supabase.table('benefits').insert(benefits_to_insert).execute()
            print(f"✓ Successfully inserted {len(benefits_to_insert)} benefits into Supabase")
            return len(benefits_to_insert)
        except Exception as e:
            print(f"✗ Error inserting benefits: {str(e)}")
            return 0
    else:
        print("No benefits to insert")
        return 0


def main():
    """Main execution function"""
    print("=" * 60)
    print("Syncing Categorized Benefits Data to Supabase")
    print("=" * 60)
    
    # Get the latest categorized file
    latest_file = get_latest_categorized_file()
    
    # Load the categorized data
    categorized_data = load_categorized_data(latest_file)
    
    print(f"\nDocument Summary: {categorized_data.get('summary', 'N/A')}")
    print(f"Total Plans Found: {categorized_data.get('total_plans_found', 'N/A')}")
    
    # Clear existing benefits (optional - comment out if you want to keep old data)
    user_input = input("\nDo you want to clear existing benefits before syncing? (yes/no): ")
    if user_input.lower() in ['yes', 'y']:
        clear_existing_benefits()
    
    # Sync benefits to Supabase
    count = sync_benefits_to_supabase(categorized_data)
    
    print("\n" + "=" * 60)
    print(f"Sync Complete! {count} benefits synced to Supabase")
    print("=" * 60)


if __name__ == "__main__":
    main()
