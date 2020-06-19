import os
import pandas
import requests

def download_file_from_google_drive(id, destination):
    """Retrieve the TPH COVID-19 spreadsheet from Google Drive."""

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    """When downloading files from Google Drive, a single GET request is not sufficient."""
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    """Saves the response to the destination file."""

    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def extract_spreadsheets_to_json(excelFile, destDir, sheet_names):
    """Extracts and converts the requested spreadsheets to JSON files."""

    for sheet_name in sheet_names:
        # Read the spreadsheet
        excel_data_df = pandas.read_excel(excelFile, sheet_name=sheet_name)
        # Convert the sheet to JSON
        json_str = excel_data_df.to_json(orient='records')
        # Save it to a file
        with open(os.path.join(destDir, sheet_name + '.json'), "w") as json_file:
            json_file.write(json_str)