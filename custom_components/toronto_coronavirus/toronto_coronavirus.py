import json
import logging
import os

from dataclasses import dataclass
from .const import DATA_PATH
# from .const import TPH_CORONAVIRUS_FILEID
from .const import TPH_CORONAVIRUS_XLSX_FILENAME
from .helpers import download_file_from_google_drive
from .helpers import extract_spreadsheets_to_json

def get_cases():
    """
    Returns an object with all of the case counts.
    e.g. {
        "all": 5,
        "active": 5,
        "recovered": 5,
        "deaths": 5,
    }
    """
    # Download and save the TPH COVID-19 spreadsheet
    # download_file_from_google_drive(TPH_CORONAVIRUS_FILEID, os.path.join(DATA_PATH, TPH_CORONAVIRUS_XLSX_FILENAME))

    # Convert the XLSX file to JSON.
    extract_spreadsheets_to_json(
        os.path.join(DATA_PATH, TPH_CORONAVIRUS_XLSX_FILENAME), 
        DATA_PATH, 
        sheet_names=["Cases", "Cumulative Cases by Episode Dat"]
    )

    cases = {}

    # if case_type in ['all', 'recovered', 'deaths']:
    with open(os.path.join(DATA_PATH, "Cases.json"), "r") as summaryFile:
        summaryData = json.load(summaryFile)
        
    for record in summaryData:
        if record["Case Type"] == "All Cases":
            cases["all"] = record["Case Count"]
        if record["Case Type"] == "Recovered":
            cases["recovered"] = record["Case Count"]
        if record["Case Type"] == "Deaths":
            cases["deaths"] = record["Case Count"]

    with open(os.path.join(DATA_PATH, "Cumulative Cases by Episode Dat.json"), "r") as episodicCasesFile:
        episodicCasesData = json.load(episodicCasesFile)

    found=False
    i = 1
    while not found and i < len(episodicCasesData):
        record = episodicCasesData[i]
        if record["Measure Names"] == "Active Cases":
            found=True
            cases["active"] = record["Measure Values"]
        i += 1
    
    return cases