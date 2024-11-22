import os
import json
import datetime
import platform
import subprocess

def is_wifi_connected():
    """
    Check if the system is connected to a WiFi network.
    """
    if platform.system() == "Windows":
        try:
            # Check the WiFi connection status
            result = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True,
                text=True
            )
            if "State" in result.stdout and "connected" in result.stdout.lower():
                # Extract SSID (WiFi name)
                for line in result.stdout.splitlines():
                    if "SSID" in line:
                        return True, line.split(":")[1].strip()
            return False, None
        except Exception as e:
            print(f"Error checking WiFi status: {e}")
            return False, None
    elif platform.system() == "Linux":
        try:
            # Linux uses nmcli to check the network connection status
            result = subprocess.run(
                ["nmcli", "-t", "-f", "ACTIVE,SSID", "dev", "wifi"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.splitlines():
                if line.startswith("yes:"):
                    return True, line.split(":")[1].strip()
            return False, None
        except Exception as e:
            print(f"Error checking WiFi status: {e}")
            return False, None
    else:
        print("This script supports only Windows and Linux.")
        return False, None

def update_wifi_status_file(is_connected, network_name):
    """
    Create or update the wifi_status.json file with the given WiFi status.
    """
    data = {
        "wifi_connected": is_connected,
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "network_name": network_name,
    }
    with open("wifi_status.json", "w") as file:
        json.dump(data, file, indent=4)
    print(f"WiFi status updated in 'wifi_status.json': {data}")

def main():
    is_connected, network_name = is_wifi_connected()
    if is_connected:
        print(f"WiFi is connected to '{network_name}'.")
        update_wifi_status_file(True, network_name)
    else:
        print("WiFi is not connected.")
        update_wifi_status_file(False, None)

if __name__ == "__main__":
    main()
