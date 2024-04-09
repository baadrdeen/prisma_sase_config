import argparse
from jinja2 import Template
import json

def rm_spaces(string):
    """Remove white spaces from a string."""
    return ''.join(char for char in string if not char.isspace())

def load_yaml_template(file_path):
    """Load YAML template from file."""
    with open(file_path, 'r') as file:
        return file.read()

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
    json_filename = f"{site_id}_site_info.json"
    
    # Load YAML template
    yaml_template = load_yaml_template(yaml_template_path)
    
        # Read the JSON file
    with open(json_filename, 'r') as json_file:
        site_info = json.load(json_file)
    
    if site_info is not None:
        # Populate data for YAML template
        data = populate_yaml_data(site_info)
        
        # Render YAML template and write to file
        render_yaml_template(yaml_template, data, output_filename)
    else:
        print("Site ID not found.")
