import os
import json
import datetime
import subprocess

def is_wifi_connected():
    """
    Check if the Raspberry Pi is connected to a WiFi network.
    """
    try:
        # Use iwconfig to get wireless information
        result = subprocess.run(
            ["iwconfig", "wlan0"],
            capture_output=True,
            text=True,
            stderr=subprocess.PIPE
        )
        
        # Check if wireless is connected
        if "Access Point:" in result.stdout:
            # Extract SSID (network name)
            for line in result.stdout.splitlines():
                if "ESSID" in line:
                    network_name = line.split('ESSID:"')[1].split('"')[0]
                    return True, network_name
        
        return False, None
    
    except Exception as e:
        print(f"Error checking WiFi status: {e}")
        return False, None

def is_internet_connected():
    """
    Check if there's an active internet connection.
    """
    try:
        # Ping Google's DNS to check internet connectivity
        result = subprocess.run(
            ["ping", "-c", "1", "8.8.8.8"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False

def update_wifi_status_file(is_connected, network_name, internet_connected):
    """
    Create or update the wifi_status.json file with the given WiFi status.
    """
    data = {
        "wifi_connected": is_connected,
        "internet_connected": internet_connected,
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "network_name": network_name or "N/A",
    }
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath("wifi_status.json")), exist_ok=True)
    
    with open("wifi_status.json", "w") as file:
        json.dump(data, file, indent=4)
    
    print(f"WiFi status updated in 'wifi_status.json': {data}")

def get_ip_address():
    """
    Retrieve the IP address of the Raspberry Pi.
    """
    try:
        result = subprocess.run(
            ["hostname", "-I"],
            capture_output=True,
            text=True
        )
        ip_addresses = result.stdout.strip().split()
        return ip_addresses[0] if ip_addresses else "N/A"
    except Exception:
        return "N/A"

def main():
    # Check WiFi connectivity
    is_connected, network_name = is_wifi_connected()
    
    # Check internet connectivity
    internet_connected = is_internet_connected()
    
    # Get IP address
    ip_address = get_ip_address()
    
    if is_connected:
        print(f"WiFi is connected to '{network_name}'.")
        print(f"IP Address: {ip_address}")
        print(f"Internet Connection: {'Available' if internet_connected else 'Unavailable'}")
    else:
        print("WiFi is not connected.")
    
    # Update status file with detailed information
    update_wifi_status_file(is_connected, network_name, internet_connected)

if __name__ == "__main__":
    main()