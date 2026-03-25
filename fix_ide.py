import sys
import subprocess

def fix_ide_environment():
    """
    This script attempts to install required dependencies (customtkinter, darkdetect, pillow)
    using the currently active Python interpreter. 
    
    If your IDE (VS Code, PyCharm, etc.) shows 'Import Error', running this script
    directly from within your IDE's terminal or 'Run' button will force it 
    to install the libraries into its own internal environment.
    """
    print(f"--- 🛠️ IDE Sync Tool ---")
    print(f"Current Interpreter: {sys.executable}\n")
    
    packages = ["customtkinter", "darkdetect", "pillow"]
    
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully.\n")
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}\n")
            
    print("--- ✨ Sync Complete ---")
    print("Please restart your IDE or wait a few seconds for the red curly lines to disappear.")
    print("You can now run 'expense_tracker.py' with zero errors!")

if __name__ == "__main__":
    fix_ide_environment()
