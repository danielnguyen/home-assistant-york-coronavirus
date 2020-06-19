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
    
    # replacing blank spaces with '_' in column headers
    data.columns =[column.replace(" ", "_") for column in data.columns] 
    
    # get rid of all other data except for Municipality of interest. 
    data.query("Municipality == 'Markham'", inplace = True)

    cases = {}
        
    cases["all"] = data.count()
    cases["active"] = data.query("Status == 'Hospitalized' and Status == 'Self-Isolating' and Status == 'Under Investigation'", inplace = False)
    cases["recovered"] = data.query("Status == 'Resolved'", inplace = False)
    cases["deaths"] = data.query("Status == 'Deceased'", inplace = False)
    
    return cases