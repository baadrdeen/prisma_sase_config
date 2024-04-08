import argparse
from jinja2 import Template
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def rm_spaces(string):
    """Remove white spaces from a string."""
    return ''.join(char for char in string if not char.isspace())

def load_yaml_template(file_path):
    """Load YAML template from file."""
    with open(file_path, 'r') as file:
        return file.read()

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

    # Assuming the second row is the header
    headers = values[2]
    # Convert rows to list of dicts
    data = [dict(zip(headers, row)) for row in values[1:]]

    # Find site information based on site_id
    for site in data:
        if site.get('Site_ID') == site_id:
            return site
    
    return None  # Site ID not found

def populate_yaml_data(site_info):
    """Populate data for rendering YAML template."""

    """ 
    
    Create the data mapping matrix by aligning the structure of your Jinja2 template with that of the source data file

    
    """
    
    return data

def render_yaml_template(yaml_template, data, output_filename):
    """Render YAML template with provided data and write to file."""
    template = Template(yaml_template)
    rendered_yaml = template.render(data)
    with open(output_filename, 'w') as file:
        file.write(rendered_yaml)
    print("YAML Site template file "+ output_filename +" generated successfully !")

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Generate YAML template file for a given site ID")
    parser.add_argument("site_id", type=str, help="Site ID to generate YAML template for")
    args = parser.parse_args()
    
    site_id = args.site_id
    yaml_template_path = "template.jinja2"
    output_filename = f"{site_id}_Branch_config.yml"
    # The scope for the Sheets API
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    # The ID of your spreadsheet
    SPREADSHEET_ID = 'Your SPREADSHEET_ID'
    # The range of cells to read from.
    RANGE_NAME = 'YOUR RANGE_NAME'
    
    # Load YAML template
    yaml_template = load_yaml_template(yaml_template_path)
    
    # Get site information from Google Sheets
    site_info = get_site_info_from_google_sheets(site_id)
    
    if site_info is not None:
        # Populate data for YAML template
        data = populate_yaml_data(site_info)
        
        # Render YAML template and write to file
        render_yaml_template(yaml_template, data, output_filename)
    else:
        print("Site ID not found.")
