"""Consts"""
DOMAIN = "york_coronavirus"
DOMAIN_DATA = "{}_data".format(DOMAIN)
VERSION = "0.0.1"
REQUIRED_FILES = ["sensor.py", "const.py", "york_coronavirus.py"]
ISSUE_URL = "https://github.com/danielnguyen/home-assistant-york-coronavirus/issues"
PLATFORMS = ["sensor"]

CONF_MUNICIPALITIES = "municipalities"

DATA_PATH = "/data"
YR_CORONAVIRUS_CSV_FILENAME = "YR_CaseData.csv"
STARTUP = """
----------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
----------------------------------------------
"""
