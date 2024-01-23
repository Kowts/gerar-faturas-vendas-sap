from datetime import datetime
import subprocess
import re
import os


def generate_template(template, variables):
    """
    Generate a string by substituting variables into a template.

    Args:
        template (str): The template string with placeholders for variables.
        variables (dict): A dictionary containing the variable names and their values.

    Returns:
        str: The generated string with variables substituted.
    """
    return template.format(**variables)



def convert_date(date_str):
    """
    Convert a date string from the format 'dd/mm/yyyy' to Portuguese format 'dd de Month'.

    Args:
    date_str (str): The date string in the format 'dd/mm/yyyy'.

    Returns:
    str: The date string in the format 'dd de Month' in Portuguese.
    """
    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")

    # Dictionary for translating months to Portuguese
    months_in_portuguese = {
        "January": "Janeiro", "February": "Fevereiro", "March": "Março",
        "April": "Abril", "May": "Maio", "June": "Junho",
        "July": "Julho", "August": "Agosto", "September": "Setembro",
        "October": "Outubro", "November": "Novembro", "December": "Dezembro"
    }

    # Formatting the date to 'dd de Month' format
    formatted_date = date_obj.strftime("%d de %B")

    # Extracting the month in English
    month_english = date_obj.strftime("%B")

    # Replacing the English month with the Portuguese equivalent
    return formatted_date.replace(month_english, months_in_portuguese[month_english])


def is_valid_email(email):
    """
    Validate an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email address is valid, False otherwise.
    """
    # Regex for validating an email address
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def is_image_file(filepath):
    """
    Check if a file is an image based on its extension.

    Parameters:
    - filepath: The path of the file to check.

    Returns:
    - True if the file is an image, False otherwise.
    """
    # Define a set of common image file extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}

    # Extract the file extension and check if it is in the set
    _, ext = os.path.splitext(filepath)
    return ext.lower() in image_extensions


def json_to_html(json_data):
    """Converts JSON data to an HTML table.

    Args:
        json_data: A dictionary containing the JSON data or None.

    Returns:
        str: The HTML representation of the JSON data as a table.
    """

    if json_data is None:
        return "<html><body><h1>Error Report</h1><p>No data available to display.</p></body></html>"

    html = "<html><body><h1>Error Report</h1><table border='1'>"
    for key, value in json_data.items():
        html += f"<tr><th>{key}</th><td>{value}</td></tr>"
    html += "</table></body></html>"
    return html


async def get_ad_user(identity: str = None, email: str = None):
    """
    Retrieve and parse Active Directory user information.

    This function executes a PowerShell command to retrieve properties of an Active Directory user
    specified by their identity. The output is then parsed to extract key-value pairs from the data.

    The PowerShell output is decoded from bytes to a string using various encodings. The parsed data is returned as a dictionary of properties.

    Args:
    identity (str): The identity of the Active Directory user.

    Returns:
    dict: A dictionary containing the parsed user properties.

    Raises:
    Exception: If the PowerShell command execution fails or returns an error.
    """
    # Format the PowerShell command with the provided identity
    if identity:
        command = f"Get-ADUser -Identity {identity} -Properties *"
    elif email:
        command = f"Get-ADUser -Filter {{Emailaddress -eq '{email}'}} -Properties *"
    else:
        raise Exception("No identity or email provided.")

    # Execute the PowerShell command
    result = subprocess.run(
        ["powershell", "-Command", command], capture_output=True)

    if result.returncode != 0:
        error_message = result.stderr.decode('utf-8', errors='replace')
        raise Exception(f"Error: {error_message}")

    # List of possible encodings
    encodings = ['utf-8', 'windows-1252', 'iso-8859-1', 'cp850']

    # Try decoding with different encodings
    for encoding in encodings:
        try:
            output = result.stdout.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise Exception("Failed to decode output with known encodings.")

    # Split the output into lines and parse it into a dictionary
    lines = output.strip().split('\n')
    parsed_data = {}
    for line in lines:
        parts = line.split(':', 1)
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            parsed_data[key] = value

    return parsed_data
