#!/usr/bin/env python3
"""
Startup script for Debugger AI
Handles environment setup and starts the FastAPI server
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def check_environment():
    """Check if virtual environment and dependencies are set up"""
    try:
        import fastapi
        import uvicorn
        import httpx
        import google.generativeai
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path(".env")
    if not env_file.exists():
        print("✗ .env file not found. Please copy .env.template to .env and configure it.")
        return False
    
    # Read and check for required variables    with open(env_file) as f:
        content = f.read()
        if "your-gemini-api-key-here" in content:
            print("✗ Please configure your Gemini API key in .env file")
            return False
    
    print("✓ .env file configured")
    return True

async def test_apis():
    """Test API connections"""
    try:
        from app.utils.setup_utils import DebuggerAIUtils
        results = await DebuggerAIUtils.test_all_connections()
        
        all_good = True
        for service, result in results.items():
            if not result['success'] and service == 'gemini':
                all_good = False
                print(f"✗ {service}: {result['message']}")
            elif not result['success']:
                print(f"⚠ {service}: {result['message']} (optional)")
        
        return all_good
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting Debugger AI server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
    print("🔧 To stop the server, press Ctrl+C")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

async def main():
    """Main startup sequence"""
    print("🤖 Debugger AI Startup Script")
    print("=" * 40)
    
    # Check dependencies
    if not check_environment():
        print("\n💡 Install dependencies with: pip install -r requirements.txt")
        return
    
    # Check configuration
    if not check_env_file():
        print("\n💡 Configure your .env file before starting")
        return
    
    # Test API connections
    print("\n🔗 Testing API connections...")
    if not await test_apis():
        print("\n⚠️  Some APIs failed to connect. Server will start but functionality may be limited.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Start server
    start_server()

if __name__ == "__main__":
    # Change to the backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Run the startup sequence
    asyncio.run(main())
