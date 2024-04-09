import argparse
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import ipaddress
import json

def get_site_info_from_google_sheets(site_id):
    """Retrieve site information based on site_id from Google Sheets data."""
    creds = None
    # Load credentials from the service account key JSON file
    creds = Credentials.from_service_account_file(
        'GCP-API-key.json', scopes=SCOPES)

    # Build the service
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return None

    # Assuming the first row is the header
    headers = values[2]
    # Convert rows to list of dicts
    data = [dict(zip(headers, row)) for row in values[1:]]

    # Find site information based on site_id
    for site in data:
        if site.get('Site_ID') == site_id:
            return site
    
    return None  # Site ID not found

def validate_site_info(site_info):
    """Validate site information."""
    fields_to_check = [
       """

        List of fields to check

       """
    ]

    ip_fields = [""" 
                            List of ip_fields
                """]

    for field in fields_to_check:
        if field in ip_fields:
            ip_value = rm_spaces(site_info[field])
            if not is_valid_ip(ip_value):
                print(f"Invalid IP address format for field '{field}': '{site_info[field]}'")
                return False
        if not site_info.get(field):
            print(f"Field '{field}' is empty.")
            return False
    
    return True

def is_valid_ip(ip):
    """Check if a string is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_subnet(subnet):
    """Check if a string contains valid subnets in CIDR notation."""
    subnets = subnet.split("\n")
    for s in subnets:
        s = s.strip()  # Strip leading/trailing whitespace
        try:
            ipaddress.ip_network(s)
        except ValueError:
            return False
    return True


def is_valid_ip_list(ip_list):
    """Check if a string contains valid IP addresses."""
    ips = ip_list.split("\n")
    for ip in ips:
        if not is_valid_ip(ip):
            return False
    return True

def rm_spaces(string):
    """Remove white spaces from a string."""
    return ''.join(char for char in string if not char.isspace())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve and validate site information from Google Sheets")
    parser.add_argument("site_id", type=str, help="Site ID to retrieve information for")
    args = parser.parse_args()

    site_id = args.site_id

    # The scope for the Sheets API
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    # The ID of your spreadsheet
    SPREADSHEET_ID = 'Your SPREADSHEET_ID'
    # The range of cells to read from.
    RANGE_NAME = 'YOUR RANGE_NAME'
    
    # Get site information from Google Sheets
    site_info = get_site_info_from_google_sheets(site_id)
    
    if site_info is not None:
        if validate_site_info(site_info):
            print("Site information is valid.")
            # Save to JSON file
            json_filename = f"{site_id}_site_info.json"
            with open(json_filename, 'w') as json_file:
                json.dump(site_info, json_file, indent=4)
            print(f"Site information saved to {json_filename}.")
        else:
            raise ValueError("Site information is invalid.")
    else:
        raise ValueError("Site ID not found.")
