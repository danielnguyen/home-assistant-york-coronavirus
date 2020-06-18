"""
A component which pulls down the daily Toronto Public Health COVID-19 updates.
For more details about this component, please refer to the documentation at
https://github.com/danielnguyen/home-assistant-toronto-covid19
"""
import excel2json
import logging
import re
import requests
import voluptuous as vol

from datetime import timedelta
from dateutil import parser

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME)
from .helpers import download_file_from_google_drive

__version__ = '0.0.1'
_LOGGER = logging.getLogger(__name__)


# - platform: toronto_covid19
#     name: Toronto COVID-19 active case count
#     case_type: summary | active | recovered | deaths

REQUIREMENTS = ['toronto_covid19']

# Configuration keys
CONF_CASE_TYPE = 'case_type'
CONF_NAME = 'name'

DEFAULT_SCAN_INTERVAL = timedelta(hours=1)
SCAN_INTERVAL = timedelta(hours=1)
COMPONENT_REPO = 'https://github.com/danielnguyen/home-assistant-toronto-covid19/'
ICON = 'mdi:hospital-box'

# Static values
TPH_COVID19_GDRIVE_FILE_ID = '1euhrML0rkV_hHF1thiA0G5vSSeZCqxHY'
TPH_COVID19_DEST_FILE_PATH = '/data/CityofToronto_COVID-19_Data.xlsx'

# If defined, the component will be treated as an entity component.
# https://developers.home-assistant.io/docs/configuration_yaml_index#platform_schema
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_CASE_TYPE): cv.string,
    vol.Optional(CONF_NAME, default='Toronto COVID-19 case count'): cv.string,
})

# Configure and add devices
async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    async_add_devices([TorontoCovid19Sensor(
        case_type=config[CONF_CASE_TYPE],
        name=config[CONF_NAME]
    )], True)


class TorontoCovid19Sensor(Entity):
    
    def __init__(self, name: str, case_type: str):
        case_counts =  {}
        self._name = name
        self._state = None
        self.case_type = case_type

    @property
    def icon(self):
        return ICON

    @property
    def name(self):
        return self._name
    
    @property
    def state(self):
        return self._state

    def update(self):
        """
        Updates the state. Called by Hass when Entity.schedule_update_ha_state(force_refresh=False) or
        Entity.async_schedule_update_ha_state(force_refresh=False) is called.
        """
        # Download and save the TPH COVID-19 spreadsheet
        download_file_from_google_drive(TPH_COVID19_GDRIVE_FILE_ID, TPH_COVID19_DEST_FILE_PATH)

        # Convert the XLSX file to JSON.
       excel2json.convert_from_file(TPH_COVID19_DEST_FILE_PATH)


        if (self.case_type == 'summary')
            self._attr = {
                "date": 1592353671487
                "all": 5
                "active": 4
                "recovered": 3
                "deaths": 2
            }
        else
            case_counts = []
            if (self.case_type == 'active')
                case_counts = [1, 2, 3, 4, 5]
            elif (self.case_type == 'recovered')
                case_counts = [1, 2, 3, 2, 1]
            elif (self.case_type == 'deaths')
                case_counts = [5, 4, 3, 2, 1]

            self._attr = {
                "case_counts": case_counts
            }

    @property
    def device_state_attributes(self):
        """Return the device attributes/data to Hass."""
        return self._attr
    
    async def async_added_to_hass(self):
        # Subscribe to add to hass callback. If entity disabled, remove subscription
        self.async_on_remove(
            self.coordinator.async_add_listener(
                self.async_write_ha_state
            )
        )
