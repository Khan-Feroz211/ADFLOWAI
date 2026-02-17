"""
ADFLOWAI - Usage Examples & Demo
Demonstrates how to use the platform programmatically
"""

import requests
from datetime import datetime, timedelta
import json

# ============================================================================
# Configuration
# ============================================================================

API_BASE_URL = "http://localhost:5000/api/v1"
API_KEY = "your-api-key-here"  # Get this after login

# Set up headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


# ============================================================================
# Example 1: Create a Multi-Platform Campaign
# ============================================================================

def example_create_campaign():
    """
    Create a new campaign across multiple platforms
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Creating Multi-Platform Campaign")
    print("="*60)
    
    # Campaign data
    campaign_data = {
        "name": "Summer Product Launch 2026",
        "description": "Major product launch campaign for Q2",
        "total_budget": 10000.00,
        "platforms": ["google_ads", "facebook", "instagram"],
        "start_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "objective": "conversions",
        "target_audience": {
            "age_range": "25-45",
            "interests": ["technology", "gadgets", "innovation"],
            "locations": ["US", "UK", "CA"],
            "gender": "all"
        }
    }
    
    # Create campaign
    response = requests.post(
        f"{API_BASE_URL}/campaigns",
        headers=headers,
        json=campaign_data
    )
    
    if response.status_code == 201:
        campaign = response.json()['campaign']
        print(f"✓ Campaign created successfully!")
        print(f"  Campaign ID: {campaign['id']}")
        print(f"  Name: {campaign['name']}")
        print(f"  Budget: ${campaign['total_budget']:,.2f}")
        print(f"  Platforms: {len(campaign_data['platforms'])}")
        return campaign['id']
    else:
        print(f"✗ Error: {response.json().get('error')}")
        return None


# ============================================================================
# Example 2: Update Campaign Metrics
# ============================================================================

def example_update_metrics(campaign_id):
    """
    Update campaign performance metrics
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Updating Campaign Metrics")
    print("="*60)
    
    # Simulated metrics after 1 week
    metrics = {
        "impressions": 50000,
        "clicks": 1500,
        "conversions": 75,
        "spent_budget": 2500.00,
        "ctr": 0.03,  # 3% CTR
        "cpc": 1.67,  # $1.67 per click
        "cpa": 33.33,  # $33.33 per acquisition
        "roas": 3.5   # 3.5x return on ad spend
    }
    
    response = requests.post(
        f"{API_BASE_URL}/campaigns/{campaign_id}/metrics",
        headers=headers,
        json=metrics
    )
    
    if response.status_code == 200:
        print("✓ Metrics updated successfully!")
        print(f"  Impressions: {metrics['impressions']:,}")
        print(f"  Clicks: {metrics['clicks']:,}")
        print(f"  Conversions: {metrics['conversions']}")
        print(f"  CTR: {metrics['ctr']*100:.2f}%")
        print(f"  ROAS: {metrics['roas']}x")
    else:
        print(f"✗ Error: {response.json().get('error')}")


# ============================================================================
# Example 3: Run AI Optimization
# ============================================================================

def example_optimize_campaign(campaign_id):
    """
    Trigger AI optimization for a campaign
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Running AI Optimization")
    print("="*60)
    
    response = requests.post(
        f"{API_BASE_URL}/campaigns/{campaign_id}/optimize",
        headers=headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✓ Optimization completed successfully!")
        print(f"  Actions taken: {len(result['actions_taken'])}")
        print("\n  Recommendations:")
        for i, action in enumerate(result['actions_taken'], 1):
            print(f"    {i}. {action}")
    else:
        print(f"✗ Error: {response.json().get('error')}")


# ============================================================================
# Example 4: Get Campaign Analytics
# ============================================================================

def example_get_analytics(campaign_id):
    """
    Retrieve comprehensive campaign analytics
    """
    print("\n" + "="*60)
    print("EXAMPLE 4: Fetching Campaign Analytics")
    print("="*60)
    
    response = requests.get(
        f"{API_BASE_URL}/campaigns/{campaign_id}/analytics",
        headers=headers
    )
    
    if response.status_code == 200:
        analytics = response.json()['analytics']
        summary = analytics['summary']
        
        print("✓ Analytics retrieved successfully!")
        print("\n  Campaign Performance:")
        print(f"    Total Impressions: {summary['total_impressions']:,}")
        print(f"    Total Clicks: {summary['total_clicks']:,}")
        print(f"    Total Conversions: {summary['total_conversions']}")
        print(f"    Total Spent: ${summary['total_spent']:,.2f}")
        print(f"    Budget Remaining: ${summary['budget_remaining']:,.2f}")
        print(f"    Performance Score: {summary['performance_score']:.2f}/1.00")
        print(f"    ROI: {summary['roi']*100:.1f}%")
        
        print("\n  Platform Breakdown:")
        for platform in analytics['platforms']:
            print(f"    {platform['platform'].upper()}:")
            print(f"      Budget: ${platform['allocated_budget']:,.2f}")
            print(f"      Spent: ${platform['spent_budget']:,.2f}")
            print(f"      Performance: {platform['performance_score']:.2f}")
    else:
        print(f"✗ Error: {response.json().get('error')}")


# ============================================================================
# Example 5: Get Dashboard Overview
# ============================================================================

def example_get_dashboard():
    """
    Get overall dashboard with all campaigns
    """
    print("\n" + "="*60)
    print("EXAMPLE 5: Dashboard Overview")
    print("="*60)
    
    response = requests.get(
        f"{API_BASE_URL}/dashboard",
        headers=headers
    )
    
    if response.status_code == 200:
        dashboard = response.json()['dashboard']
        
        print("✓ Dashboard data retrieved successfully!")
        print("\n  Overall Statistics:")
        print(f"    Total Campaigns: {dashboard['total_campaigns']}")
        print(f"    Active Campaigns: {dashboard['active_campaigns']}")
        print(f"    Paused Campaigns: {dashboard['paused_campaigns']}")
        print(f"    Total Budget: ${dashboard['total_budget']:,.2f}")
        print(f"    Total Spent: ${dashboard['total_spent']:,.2f}")
        print(f"    Budget Remaining: ${dashboard['budget_remaining']:,.2f}")
        print(f"    Average CTR: {dashboard['avg_ctr']:.2f}%")
        print(f"    Average Performance: {dashboard['avg_performance_score']:.2f}")
        
        print("\n  Top 5 Performing Campaigns:")
        for i, campaign in enumerate(dashboard['top_campaigns'][:5], 1):
            print(f"    {i}. {campaign['name']} (Score: {campaign['performance_score']:.2f})")
    else:
        print(f"✗ Error: {response.json().get('error')}")


# ============================================================================
# Example 6: List All Campaigns with Filters
# ============================================================================

def example_list_campaigns(status=None):
    """
    List all campaigns with optional status filter
    """
    print("\n" + "="*60)
    print(f"EXAMPLE 6: Listing Campaigns {f'(Status: {status})' if status else ''}")
    print("="*60)
    
    params = {}
    if status:
        params['status'] = status
    
    response = requests.get(
        f"{API_BASE_URL}/campaigns",
        headers=headers,
        params=params
    )
    
    if response.status_code == 200:
        result = response.json()
        campaigns = result['campaigns']
        
        print(f"✓ Found {result['count']} campaigns")
        print("\n  Campaigns:")
        for campaign in campaigns:
            status_emoji = "🟢" if campaign['status'] == 'active' else "🟡" if campaign['status'] == 'paused' else "⚫"
            print(f"    {status_emoji} {campaign['name']}")
            print(f"       ID: {campaign['id']} | Budget: ${campaign['total_budget']:,.2f} | Score: {campaign['performance_score']:.2f}")
    else:
        print(f"✗ Error: {response.json().get('error')}")


# ============================================================================
# Example 7: Real-World Scenario - Complete Workflow
# ============================================================================

def example_complete_workflow():
    """
    Demonstrates a complete campaign lifecycle
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Complete Campaign Workflow")
    print("="*70)
    print("\nThis example demonstrates a full campaign lifecycle:")
    print("  1. Create campaign")
    print("  2. Simulate 1 week of performance")
    print("  3. Run AI optimization")
    print("  4. View results")
    print("="*70)
    
    # Step 1: Create campaign
    print("\n📝 Step 1: Creating campaign...")
    campaign_id = example_create_campaign()
    
    if not campaign_id:
        print("✗ Failed to create campaign. Stopping workflow.")
        return
    
    input("\nPress Enter to continue to Step 2...")
    
    # Step 2: Update metrics (simulating 1 week)
    print("\n📊 Step 2: Updating metrics after 1 week...")
    example_update_metrics(campaign_id)
    
    input("\nPress Enter to continue to Step 3...")
    
    # Step 3: Run optimization
    print("\n🤖 Step 3: Running AI optimization...")
    example_optimize_campaign(campaign_id)
    
    input("\nPress Enter to continue to Step 4...")
    
    # Step 4: View analytics
    print("\n📈 Step 4: Viewing final analytics...")
    example_get_analytics(campaign_id)
    
    print("\n" + "="*70)
    print("✓ Complete workflow demonstration finished!")
    print("="*70)


# ============================================================================
# Main Menu
# ============================================================================

def main():
    """
    Interactive demo menu
    """
    print("\n" + "="*70)
    print("        ADFLOWAI - Interactive Demo & Examples")
    print("        AI-Powered Campaign Optimization Platform")
    print("="*70)
    
    print("\n⚠️  IMPORTANT: Make sure to:")
    print("  1. Start the ADFLOWAI server: python app.py")
    print("  2. Have a valid API key (get one after login)")
    print("  3. Update API_KEY in this file")
    
    while True:
        print("\n" + "-"*70)
        print("Select an example to run:")
        print("  1. Create a multi-platform campaign")
        print("  2. Update campaign metrics")
        print("  3. Run AI optimization")
        print("  4. Get campaign analytics")
        print("  5. View dashboard overview")
        print("  6. List all campaigns")
        print("  7. Complete workflow (recommended for first-time)")
        print("  8. Run all examples")
        print("  0. Exit")
        print("-"*70)
        
        choice = input("\nEnter your choice [0-8]: ").strip()
        
        if choice == "0":
            print("\n👋 Thanks for trying ADFLOWAI! Visit us at https://adflowai.com")
            break
        elif choice == "1":
            example_create_campaign()
        elif choice == "2":
            campaign_id = input("Enter campaign ID: ").strip()
            example_update_metrics(int(campaign_id))
        elif choice == "3":
            campaign_id = input("Enter campaign ID: ").strip()
            example_optimize_campaign(int(campaign_id))
        elif choice == "4":
            campaign_id = input("Enter campaign ID: ").strip()
            example_get_analytics(int(campaign_id))
        elif choice == "5":
            example_get_dashboard()
        elif choice == "6":
            status = input("Filter by status (active/paused/stopped) or press Enter for all: ").strip()
            example_list_campaigns(status if status else None)
        elif choice == "7":
            example_complete_workflow()
        elif choice == "8":
            print("\n🚀 Running all examples...")
            example_create_campaign()
            input("\nPress Enter to continue...")
            example_get_dashboard()
            input("\nPress Enter to continue...")
            example_list_campaigns()
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
