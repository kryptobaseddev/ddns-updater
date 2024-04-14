import os
import requests
import time
import json
import logging
import sys
import xml.etree.ElementTree as ET
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Ensure logs directory exists
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

# Load environment variables from .env file
load_dotenv()

# Configuration file for DNS providers
CONFIG_FILE = "config.json"

# Set up logging
LOG_FILE = os.path.join(LOG_DIR, 'ddns_updater.log')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - [%(levelname)s] - %(message)s', stream=sys.stdout)
handler = RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)
handler.setLevel(logging.DEBUG)

# Customize log format with log level prefixes
formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    
# Function to extract relevant info from interface-response XML
def parse_interface_response(response_text):
    root = ET.fromstring(response_text)
    ip = root.find("IP").text
    done = root.find("Done").text
    return ip, done

def update_dns(provider_config, domain, password, subdomains, ip):
    url = f"{provider_config['api_url']}?domain={domain}&password={password}&ip={ip}"

    for subdomain in subdomains.split(","):
        subdomain = subdomain.strip()
        request_url = f"{url}&host={subdomain}"
        response = requests.get(request_url)

        logging.debug(f"API Request URL: {request_url}")
        logging.debug(f"API Response: {response.text}")

        if "<ErrCount>" in response.text:
            error_msg_index = response.text.find("<Err1>")
            if error_msg_index != -1:
                error_msg = response.text[error_msg_index + len("<Err1>"):]
                error_msg_end_index = error_msg.find("</Err1>")
                if error_msg_end_index != -1:
                    error_msg = error_msg[:error_msg_end_index]
                logging.error(f"Error message from API: {error_msg}")
                print(f"ERROR: {error_msg}")
                exit(1)
            else:
                new_ip, done = parse_interface_response(response.text)
                if done == 'true':
                    logging.info(f"Subdomain {subdomain}.{domain} IP updated to: {new_ip}")
                else:
                    logging.info(f"Subdomain {subdomain}.{domain} IP remains the same: {new_ip}")
        else:
            logging.error("Error: IP not found in API response")
            print("Error: IP not found in API response")
            exit(1)

def show_help():
    print("""
Usage: python ddns-updater.py [-h] [-d DOMAIN] [-s SUBDOMAINS] [-p PASSWORD] [-i IP] [-t INTERVAL]

Options:
  -h               Display this help message
  -d DOMAIN        Domain name
  -s SUBDOMAINS    Comma-separated list of subdomains
  -p PASSWORD      Dynamic DNS password for the domain
  -i IP            IP address to set (optional)
  -t INTERVAL      Interval for updating DNS records in seconds (default: 3600)
""")

def main():
    config = load_config()
    provider = os.getenv("DNS_PROVIDER")
    provider_config = config.get("providers", {}).get(provider)
    if not provider_config:
        logging.error("Invalid DNS provider specified.")
        print("Error: Invalid DNS provider specified.")
        exit(1)
    
    required_fields = provider_config.get("required_fields", [])
    missing_fields = [field for field in required_fields if not os.getenv(field.upper())]
    if missing_fields:
        logging.error(f"Missing required fields for {provider}: {', '.join(missing_fields)}")
        print(f"Error: Missing required fields for {provider}: {', '.join(missing_fields)}")
        exit(1)

    # Run DNS update logic
    interval_seconds = get_interval_seconds()
    while True:
        run_dns_update(provider_config)
        print_countdown(interval_seconds)

def get_interval_seconds():
    interval = os.getenv("INTERVAL", "3600")
    try:
        return int(interval.rstrip('s'))  # Remove 's' and convert to int
    except ValueError:
        logging.error("Invalid interval format. Using default interval of 3600 seconds.")
        return 3600

def run_dns_update(provider_config):
    domain = os.getenv("DOMAIN")
    password = os.getenv("PASSWORD")
    subdomains = os.getenv("SUBDOMAINS")
    ip = os.getenv("IP", requests.get("https://ifconfig.me").text.strip())
    update_dns(provider_config, domain, password, subdomains, ip)

def print_countdown(interval_seconds):
    try:
        for remaining_time in range(interval_seconds, 0, -1):
            days, remaining_time = divmod(remaining_time, 86400)
            hours, remaining_time = divmod(remaining_time, 3600)
            minutes, remaining_time = divmod(remaining_time, 60)
            seconds = remaining_time
            print("\r" + " " * 80, end='', flush=True)  # Clear the current line
            print(f"\rNext update in: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds", end='', flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the script...")
        sys.exit(0)

if __name__ == "__main__":
    main()
