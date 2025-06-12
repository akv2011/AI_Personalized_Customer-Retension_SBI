#!/usr/bin/env python3
"""
Real-time Monitoring Dashboard for SBI Chatbot
Shows live statistics and health metrics
"""

import asyncio
import sys
import os
import time
import json
from datetime import datetime, timedelta
import requests

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

BASE_URL = "http://127.0.0.1:5000"

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def get_system_status():
    """Get overall system status"""
    try:
        response = requests.get(f"{BASE_URL}/api/database/status")
        if response.status_code == 200:
            return response.json()
        return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_analytics():
    """Get analytics data"""
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/summary?days=1")
        if response.status_code == 200:
            return response.json()
        return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_recent_operations():
    """Get recent MCP operations"""
    try:
        response = requests.get(f"{BASE_URL}/api/mcp/operations?limit=10")
        if response.status_code == 200:
            return response.json()
        return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def format_timestamp(timestamp_str):
    """Format timestamp for display"""
    try:
        if timestamp_str:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime('%H:%M:%S')
        return "N/A"
    except:
        return "N/A"

def get_status_emoji(status):
    """Get emoji for status"""
    if status == True or status == "operational":
        return "🟢"
    elif status == False or status == "error":
        return "🔴"
    else:
        return "🟡"

def display_dashboard():
    """Display the monitoring dashboard"""
    clear_screen()
    
    # Header
    print("🚀 SBI LIFE CHATBOT - REAL-TIME MONITORING DASHBOARD")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Press Ctrl+C to exit)")
    print("=" * 70)
    
    # System Status
    print("\n🏥 SYSTEM HEALTH")
    print("-" * 50)
    
    status = get_system_status()
    if "error" in status:
        print(f"❌ System Error: {status['error']}")
        print("   🔧 Please check if Flask server is running")
    else:
        db_available = status.get('database_available', False)
        db_healthy = status.get('database_healthy', False) 
        mcp_status = status.get('mcp_server', 'unknown')
        
        print(f"🗄️  Database Available: {get_status_emoji(db_available)} {db_available}")
        print(f"💚 Database Healthy:   {get_status_emoji(db_healthy)} {db_healthy}")
        print(f"🔧 MCP Server:         {get_status_emoji(mcp_status=='operational')} {mcp_status}")
    
    # Analytics
    print("\n📊 TODAY'S ANALYTICS")
    print("-" * 50)
    
    analytics = get_analytics()
    if "error" in analytics:
        print(f"❌ Analytics Error: {analytics['error']}")
    else:
        data = analytics.get('analytics', {})
        print(f"💬 Total Interactions:  {data.get('total_interactions', 0)}")
        print(f"👥 Unique Customers:    {data.get('unique_customers', 0)}")
        print(f"😊 Positive Sentiment:  {data.get('positive_interactions', 0)}")
        print(f"😐 Neutral Sentiment:   {data.get('neutral_interactions', 0)}")
        print(f"😞 Negative Sentiment:  {data.get('negative_interactions', 0)}")
    
    # Recent Operations
    print("\n🔧 RECENT MCP OPERATIONS")
    print("-" * 50)
    
    operations = get_recent_operations()
    if "error" in operations:
        print(f"❌ Operations Error: {operations['error']}")
    else:
        ops = operations.get('operations', [])
        if ops:
            print(f"📋 Showing last {len(ops)} operations:")
            print()
            for op in ops[:5]:  # Show last 5
                timestamp = format_timestamp(op.get('created_at'))
                op_type = op.get('operation_type', 'unknown')[:20]
                status = op.get('status', 'unknown')
                exec_time = op.get('execution_time_ms', 0)
                
                status_emoji = "✅" if status == "success" else "❌" if status == "error" else "🟡"
                print(f"   {status_emoji} {timestamp} | {op_type:<20} | {exec_time:>4}ms | {status}")
        else:
            print("   📭 No recent operations found")
    
    # Performance Metrics
    print("\n⚡ PERFORMANCE METRICS")
    print("-" * 50)
    
    if "error" not in operations:
        ops = operations.get('operations', [])
        if ops:
            # Calculate average response time
            exec_times = [op.get('execution_time_ms', 0) for op in ops if op.get('execution_time_ms')]
            if exec_times:
                avg_time = sum(exec_times) / len(exec_times)
                max_time = max(exec_times)
                min_time = min(exec_times)
                
                print(f"📈 Avg Response Time:   {avg_time:.1f}ms")
                print(f"⚡ Min Response Time:   {min_time}ms")
                print(f"🔥 Max Response Time:   {max_time}ms")
                
                # Success rate
                successful = len([op for op in ops if op.get('status') == 'success'])
                success_rate = (successful / len(ops)) * 100 if ops else 0
                print(f"✅ Success Rate:       {success_rate:.1f}%")
            else:
                print("   📊 No performance data available")
        else:
            print("   📊 No operations data available")
    
    # Footer
    print("\n" + "=" * 70)
    print("🔄 Dashboard refreshes every 5 seconds")
    print("💡 Tip: Keep this running to monitor your chatbot health")

def main():
    """Main monitoring loop"""
    print("🚀 Starting SBI Chatbot Monitoring Dashboard...")
    print("📊 Dashboard will refresh every 5 seconds")
    print("⛔ Press Ctrl+C to stop monitoring")
    time.sleep(2)
    
    try:
        while True:
            display_dashboard()
            time.sleep(5)  # Refresh every 5 seconds
    except KeyboardInterrupt:
        clear_screen()
        print("👋 Monitoring dashboard stopped")
        print("📊 Thank you for monitoring your SBI Chatbot!")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

if __name__ == "__main__":
    main()
