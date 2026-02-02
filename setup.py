"""
Quick setup script for Trading Bot
Automates the initial configuration process
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required!")
        return False
    
    print("✅ Python version OK")
    return True


def check_git():
    """Check if Git is installed"""
    print_header("Checking Git")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        print(result.stdout.strip())
        print("✅ Git is installed")
        return True
    except FileNotFoundError:
        print("❌ Git is not installed!")
        print("Please install Git from: https://git-scm.com/downloads")
        return False


def check_freqtrade():
    """Check if Freqtrade is cloned"""
    print_header("Checking Freqtrade")
    freqtrade_path = Path("freqtrade")
    
    if freqtrade_path.exists():
        print("✅ Freqtrade directory found")
        return True
    else:
        print("⏳ Freqtrade not found, cloning repository...")
        try:
            subprocess.run(['git', 'clone', 'https://github.com/freqtrade/freqtrade.git'], check=True)
            print("✅ Freqtrade cloned successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to clone Freqtrade")
            return False


def create_venv():
    """Create virtual environment"""
    print_header("Creating Virtual Environment")
    venv_path = Path("freqtrade/.venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, '-m', 'venv', 'freqtrade/.venv'], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False


def install_requirements():
    """Install Freqtrade requirements"""
    print_header("Installing Requirements")
    
    # Determine pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = Path("freqtrade/.venv/Scripts/pip.exe")
    else:  # Linux/Mac
        pip_path = Path("freqtrade/.venv/bin/pip")
    
    if not pip_path.exists():
        print("❌ Pip not found in virtual environment")
        return False
    
    print("⏳ Installing Freqtrade (this may take a few minutes)...")
    try:
        subprocess.run([str(pip_path), 'install', '-e', 'freqtrade[all]'], check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False


def copy_config_files():
    """Copy configuration files to Freqtrade user_data"""
    print_header("Copying Configuration Files")
    
    user_data_path = Path("freqtrade/user_data")
    strategies_path = user_data_path / "strategies"
    
    # Create directories if they don't exist
    strategies_path.mkdir(parents=True, exist_ok=True)
    
    # Copy strategy
    strategy_src = Path("bot_config/GridScalpingHybrid.py")
    strategy_dst = strategies_path / "GridScalpingHybrid.py"
    
    if strategy_src.exists():
        import shutil
        shutil.copy(strategy_src, strategy_dst)
        print(f"✅ Copied strategy to {strategy_dst}")
    else:
        print("❌ Strategy file not found")
        return False
    
    # Copy config
    config_src = Path("bot_config/config.json")
    config_dst = user_data_path / "config.json"
    
    if config_src.exists():
        import shutil
        shutil.copy(config_src, config_dst)
        print(f"✅ Copied config to {config_dst}")
    else:
        print("❌ Config file not found")
        return False
    
    return True


def create_env_file():
    """Create .env file from example if it doesn't exist"""
    print_header("Setting Up Environment Variables")
    
    env_file = Path("freqtrade/.env")
    env_example = Path("bot_config/.env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print(f"✅ Created .env file")
        print("⚠️  Don't forget to edit .env with your API keys!")
        return True
    else:
        print("❌ .env.example not found")
        return False


def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete! 🎉")
    
    print("Next steps:")
    print()
    print("1. Configure your API keys:")
    print("   - Edit freqtrade/.env")
    print("   - Add your Binance API Key and Secret")
    print()
    print("2. Activate the virtual environment:")
    if os.name == 'nt':
        print("   freqtrade\\.venv\\Scripts\\activate")
    else:
        print("   source freqtrade/.venv/bin/activate")
    print()
    print("3. Test with paper trading:")
    print("   freqtrade trade --config user_data/config.json --strategy GridScalpingHybrid --dry-run")
    print()
    print("4. Run backtesting:")
    print("   freqtrade backtesting --strategy GridScalpingHybrid --timerange 20231001-20240101")
    print()
    print("5. Read the documentation:")
    print("   - README.md (this project)")
    print("   - https://www.freqtrade.io/en/stable/")
    print()
    print("⚠️  IMPORTANT: Always start with paper trading (dry-run mode)!")
    print()


def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  Trading Bot - Automated Setup")
    print("  Target: $10 USD Daily")
    print("="*60)
    
    # Run checks and setup steps
    steps = [
        ("Python Version", check_python_version),
        ("Git", check_git),
        ("Freqtrade Repository", check_freqtrade),
        ("Virtual Environment", create_venv),
        ("Python Requirements", install_requirements),
        ("Configuration Files", copy_config_files),
        ("Environment Variables", create_env_file),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_name}")
            print("Please fix the issue and run this script again.")
            sys.exit(1)
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
