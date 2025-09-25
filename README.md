# CMD Proxy Manager

A simple Python script to manage proxy settings in CMD and PowerShell environments, allowing users to set, unset, or switch between proxy profiles stored in text files.

## Features
- Set proxy settings for the current CMD or PowerShell session.
- Store and retrieve proxy configurations from a `profiles` directory.
- Persist current proxy across sessions using a `current_proxy.txt` file.
- Test proxy connectivity with a ping to a specified host (default: google.com).
- Interactive CLI mode to select profiles or disable the current proxy.
- Full CLI mode to set a specific profile via command-line arguments.
- Compatible with both CMD and PowerShell.

## Prerequisites
- Python 3.6 or higher
- Required Python package: `inquirer`
  - Install it automatically when running the script for the first time, or manually with:
    ```bash
    pip install inquirer
    ```

## Setup
1. Clone or download the repository to your local machine.
2. Create a `profiles` directory in the same directory as `proxy_manager.py`.
3. Add proxy profiles as text files in the `profiles` directory. Each file should contain a proxy address in the format `host:port` (e.g., `127.0.0.1:10809`).
   - Example: Create a file named `v2ray-http.txt` with the content `127.0.0.1:10809`.

## Usage
### Semi-CLI Mode
Run the script without arguments to enter interactive mode:
```bash
python proxy_manager.py
```
- Displays the current proxy status.
- Lists available profiles and an option to disable the current proxy (`No Proxy`).
- Select a profile to set the proxy or disable it.
- Tests connectivity with a ping to `google.com`.

### Full CLI Mode
Set a specific proxy profile directly:
```bash
python proxy_manager.py <profile_name>
```
- Example: `python proxy_manager.py v2ray-http`
- If a proxy is already set, it prompts to unset it before applying the new profile.

### Example Output
**First run (no proxy set):**
```
Current proxy: None
[?] Select a profile:
   another-profile
 > v2ray-http
Proxy set for this session: 127.0.0.1:10809
Pinging google.com: 80ms
```

**Subsequent run (proxy set):**
```
Current proxy is set: http://127.0.0.1:10809 (Profile: v2ray-http)
Pinging google.com: 75ms
[?] Select a profile:
   No Proxy (Disable Current Proxy)
   another-profile
 > v2ray-http
```

## Notes
- The script stores the current proxy in `current_proxy.txt` to persist across sessions.
- Proxy settings are applied only to the current CMD or PowerShell session.
- Ensure the `profiles` directory contains valid proxy configuration files.
- If no profiles are found, create them in the `profiles` directory as `.txt` files.

## Troubleshooting
- **Proxy not detected in PowerShell**: Ensure the script is run in the same session where the proxy was set, or check `current_proxy.txt` for the saved proxy.
- **Ping fails**: Verify that the proxy is running and correctly configured.
- **No profiles found**: Create at least one `.txt` file in the `profiles` directory with a valid proxy address.