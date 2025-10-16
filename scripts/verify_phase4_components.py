#!/usr/bin/env python3
"""
Verification script for Phase 4 components
"""

import os
from pathlib import Path

def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists and print status"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description:30} | {filepath}")
    return exists

def verify_phase4_components():
    """Verify all Phase 4 components are in place"""
    print("Phase 4 Component Verification")
    print("=" * 50)
    
    # Get project root
    project_root = Path(__file__).parent.parent
    frontend_root = project_root / "frontend"
    
    # Backend API files
    backend_files = [
        ("backend/api/main.py", "FastAPI Main Server"),
        ("backend/api/routes/bots.py", "Bot Management Routes"),
        ("backend/api/routes/strategies.py", "Strategy Routes"),
        ("backend/api/routes/analytics.py", "Analytics Routes"),
    ]
    
    # Frontend files
    frontend_files = [
        ("frontend/package.json", "Frontend Package Config"),
        ("frontend/tailwind.config.js", "TailwindCSS Config"),
        ("frontend/tsconfig.json", "TypeScript Config"),
        ("frontend/src/app/layout.tsx", "Root Layout"),
        ("frontend/src/app/page.tsx", "Main Dashboard Page"),
        ("frontend/src/app/globals.css", "Global Styles"),
        ("frontend/src/components/dashboard/DashboardHeader.tsx", "Dashboard Header"),
        ("frontend/src/components/dashboard/StatsGrid.tsx", "Stats Grid"),
        ("frontend/src/components/charts/ChartContainer.tsx", "Chart Container"),
        ("frontend/src/components/bots/BotList.tsx", "Bot List"),
        ("frontend/src/components/agents/AgentPanel.tsx", "Agent Panel"),
        ("frontend/src/components/dashboard/TradeHistory.tsx", "Trade History"),
    ]
    
    # Scripts
    script_files = [
        ("scripts/start_full_stack.sh", "Linux/Mac Start Script"),
        ("scripts/start_full_stack.bat", "Windows Start Script"),
    ]
    
    # Documentation
    doc_files = [
        ("README_PHASE4.md", "Phase 4 Documentation"),
    ]
    
    # Check all files
    all_files = backend_files + frontend_files + script_files + doc_files
    missing_files = []
    
    for filepath, description in all_files:
        full_path = project_root / filepath
        if not check_file_exists(str(full_path), description):
            missing_files.append(filepath)
    
    print("=" * 50)
    
    if not missing_files:
        print("🎉 All Phase 4 components are in place!")
        print("\nNext steps:")
        print("1. Start the backend API: make start-api")
        print("2. Start the frontend: make start-ui")
        print("3. Or start both: make start-full")
        print("4. Visit http://localhost:3000 in your browser")
        return True
    else:
        print("❌ Some components are missing:")
        for file in missing_files:
            print(f"  - {file}")
        return False

if __name__ == "__main__":
    verify_phase4_components()