import csv
import json
import logging
import os

import pandas

from dataclasses import dataclass
from .const import DATA_PATH
from .const import YR_CORONAVIRUS_CSV_FILENAME

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
    
    # Making data frame from csv file 
    data = pandas.read_csv(YR_CORONAVIRUS_CSV_FILENAME);
    
    # get rid of all other data except for Municipality of interest. 
    data.query("Municipality == 'Markham'", inplace=True)

    cases = {}
        
    cases["all"] = len(data)
    cases["active"] = len(data.query("Status == 'Hospitalized' or Status == 'Self-Isolating' or Status == 'Under Investigation'"))
    cases["recovered"] = len(data.query("Status == 'Resolved'"))
    cases["deaths"] = len(data.query("Status == 'Deceased'"))
    
    return cases