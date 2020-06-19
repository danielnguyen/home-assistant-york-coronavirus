"""Consts"""
DOMAIN = 'toronto_covid19'
DOMAIN_DATA = '{}_data'.format(DOMAIN)
VERSION = '0.0.1'
REQUIRED_FILES = ['sensor.py', 'const.py', 'toronto_coronavirus.py']
ISSUE_URL = 'https://github.com/danielnguyen/home-assistant-toronto-covid19/issues'
PLATFORMS = ['sensor']

DATA_PATH = "/data"
TPH_CORONAVIRUS_FILEID = '1euhrML0rkV_hHF1thiA0G5vSSeZCqxHY'
TPH_CORONAVIRUS_XLSX_FILENAME = "CityofToronto_COVID-19_Data.xlsx"

STARTUP = """
----------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
----------------------------------------------
"""