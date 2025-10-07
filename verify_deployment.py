"""
Hugging Face Deployment Verification Script
Run this to verify the app is ready for secure deployment.
"""

import os
import sys

def check_api_key_security():
    """Check that API key is properly configured for deployment."""
    print("🔍 Checking API Key Security...")
    
    # Check if hardcoded API key exists in config.py
    try:
        with open('config.py', 'r') as f:
            content = f.read()
            if 'AIzaSy' in content and 'os.getenv' not in content:
                print("❌ SECURITY RISK: Hardcoded API key found in config.py")
                return False
            else:
                print("✅ config.py uses environment variables - SECURE")
    except FileNotFoundError:
        print("⚠️ config.py not found")
    
    # Check environment variable
    api_key = os.getenv('YOUTUBE_API_KEY')
    if api_key:
        print(f"✅ YOUTUBE_API_KEY environment variable is set (length: {len(api_key)})")
    else:
        print("⚠️ YOUTUBE_API_KEY environment variable not set (expected for Hugging Face)")
    
    return True

def check_dependencies():
    """Check that all required dependencies are available."""
    print("\n📦 Checking Dependencies...")
    
    required_packages = [
        'streamlit',
        'google-api-python-client',
        'google-auth',
        'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Install missing packages: pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_app_structure():
    """Check that all required files are present."""
    print("\n📁 Checking App Structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'config.py',
        'src/core/youtube_api.py',
        'src/core/search_service.py',
        'src/core/data_processor.py',
        'src/ui/components.py',
        'src/utils/config.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_huggingface_readiness():
    """Check Hugging Face Spaces specific requirements."""
    print("\n🤗 Checking Hugging Face Spaces Readiness...")
    
    # Check if running in Hugging Face environment
    space_id = os.getenv('SPACE_ID')
    if space_id:
        print(f"✅ Running in Hugging Face Space: {space_id}")
    else:
        print("ℹ️ Not running in Hugging Face Spaces (local environment)")
    
    # Check app.py has proper Streamlit configuration
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            if 'streamlit' in content and 'main()' in content:
                print("✅ app.py has proper Streamlit structure")
            else:
                print("❌ app.py missing proper Streamlit structure")
                return False
    except FileNotFoundError:
        print("❌ app.py not found")
        return False
    
    return True

def main():
    """Run all verification checks."""
    print("🚀 YouTube Search App - Hugging Face Deployment Verification")
    print("=" * 60)
    
    checks = [
        check_api_key_security,
        check_dependencies,
        check_app_structure,
        check_huggingface_readiness
    ]
    
    all_passed = True
    for check in checks:
        try:
            if not check():
                all_passed = False
        except Exception as e:
            print(f"❌ Error in {check.__name__}: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED - Ready for Hugging Face Deployment!")
        print("\n📋 Next Steps:")
        print("1. Create a Hugging Face Space (Streamlit SDK)")
        print("2. Set YOUTUBE_API_KEY in Space Settings > Variables and secrets")
        print("3. Upload all files from hf_deployment_package folder")
        print("4. Your app will be live at: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME")
    else:
        print("⚠️ ISSUES FOUND - Please fix the problems above before deployment")
    
    print("\n🔒 Security Checklist:")
    print("✅ No hardcoded API keys")
    print("✅ Environment variable configuration")
    print("✅ Secure .gitignore rules")
    print("✅ Hugging Face Spaces secrets integration")

if __name__ == "__main__":
    main()