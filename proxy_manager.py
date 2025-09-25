import os
import sys
import subprocess
from pathlib import Path

try:
    import inquirer
except ImportError:
    print("Installing required package 'inquirer'...")
    os.system(f"{sys.executable} -m pip install inquirer")
    import inquirer

PROFILE_DIR = Path(__file__).parent / "profiles"
CURRENT_PROXY_FILE = Path(__file__).parent / "current_proxy.txt"

# --- Helper Functions ---
def save_current_proxy(proxy):
    """Save the current proxy to a file for persistence across sessions"""
    with open(CURRENT_PROXY_FILE, "w") as f:
        f.write(proxy)

def load_current_proxy():
    """Load the current proxy from the file"""
    if CURRENT_PROXY_FILE.exists():
        with open(CURRENT_PROXY_FILE, "r") as f:
            return f.read().strip()
    return None

def get_current_proxy():
    """Get the current proxy from environment variables or file"""
    http = os.environ.get("HTTP_PROXY", None)
    if not http:
        proxy = load_current_proxy()
        if proxy:
            http = f"http://{proxy}"
    https = os.environ.get("HTTPS_PROXY", None)
    return http, https

def set_proxy(proxy):
    """Set the proxy for the current session and save to file"""
    os.environ["HTTP_PROXY"] = f"http://{proxy}"
    os.environ["HTTPS_PROXY"] = f"http://{proxy}"
    os.system(f'set HTTP_PROXY=http://{proxy}')
    os.system(f'set HTTPS_PROXY=http://{proxy}')
    save_current_proxy(proxy)
    print(f"\nProxy set for this session: {proxy}")

def unset_proxy():
    """Remove the proxy from the current session and file"""
    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)
    os.system("set HTTP_PROXY=")
    os.system("set HTTPS_PROXY=")
    if CURRENT_PROXY_FILE.exists():
        CURRENT_PROXY_FILE.unlink()
    print("\nProxy unset for this session")

def list_profiles():
    """List all available profiles"""
    if not PROFILE_DIR.exists():
        PROFILE_DIR.mkdir()
    return [f.stem for f in PROFILE_DIR.glob("*.txt")]

def read_profile(profile):
    """Read proxy details from a profile file"""
    file_path = PROFILE_DIR / f"{profile}.txt"
    if file_path.exists():
        with open(file_path, "r") as f:
            return f.read().strip()
    return None

def ping_host(host="google.com"):
    """Test connectivity with a ping to the specified host"""
    try:
        output = subprocess.run(
            ["ping", "-n", "1", host],
            capture_output=True,
            text=True
        )
        if output.returncode == 0:
            for line in output.stdout.splitlines():
                if "Reply from" in line and "time=" in line:
                    time_ms = line.split("time=")[1].split()[0]
                    print(f"Pinging {host}: {time_ms}")
                    return
            print(f"Pinging {host} successful.")
        else:
            print("Ping failed.")
    except Exception as e:
        print(f"Ping error: {e}")

# --- Semi-CLI Mode ---
def semi_cli():
    profiles = list_profiles()
    current_http, current_https = get_current_proxy()
    menu_choices = []

    # Check current proxy status
    if current_http:
        active_profile = None
        for profile in profiles:
            proxy = read_profile(profile)
            if proxy and f"http://{proxy}" == current_http:
                active_profile = profile
                break
        if active_profile:
            print(f"Current proxy is set: {current_http} (Profile: {active_profile})")
        else:
            print(f"Current proxy is set: {current_http} (No matching profile)")
        ping_host()
        menu_choices.append("No Proxy (Disable Current Proxy)")
    else:
        print("Current proxy: None")

    menu_choices += profiles
    if not menu_choices:
        print("No profiles found! Please create profiles in the 'profiles' directory.")
        return

    questions = [
        inquirer.List(
            "profile",
            message="Select a profile",
            choices=menu_choices,
        )
    ]
    answers = inquirer.prompt(questions)
    if answers:
        choice = answers["profile"]
        if choice.startswith("No Proxy"):
            unset_proxy()
        else:
            proxy = read_profile(choice)
            if proxy:
                set_proxy(proxy)
        # Ping after setting or unsetting proxy
        current_http, _ = get_current_proxy()
        if current_http:
            ping_host()
        else:
            print("Proxy is disabled.")

# --- Full CLI Mode ---
def full_cli(profile_name):
    proxy = read_profile(profile_name)
    if not proxy:
        print(f"Profile '{profile_name}' not found!")
        return

    current_http, _ = get_current_proxy()
    if current_http:
        print(f"Current proxy is set: {current_http}")
        ping_host()
        choice = input("Do you want to unset it first? (y/N): ").lower()
        if choice == "y":
            unset_proxy()

    set_proxy(proxy)
    ping_host()

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        full_cli(sys.argv[1])
    else:
        semi_cli()