"""
A component which pulls down the daily York Region Public Health COVID-19 updates.
For more details about this component, please refer to the documentation at
https://github.com/danielnguyen/home-assistant-york-coronavirus
"""
import datetime
import logging

from datetime import timedelta
from dateutil import parser

from homeassistant.helpers.entity import Entity
from . import update_data
from .const import CONF_MUNICIPALITIES, DOMAIN_DATA, VERSION

__version__ = VERSION
_LOGGER = logging.getLogger(__name__)

CASE_TYPES = {
    "all": "mdi:hospital-box",
    "active": "mdi:emoticon-sad-outline",
    "recovered": "mdi:emoticon-happy-outline",
    "deaths": "mdi:emoticon-cry-outline"
}

DEFAULT_SCAN_INTERVAL = timedelta(hours=1)
SCAN_INTERVAL = timedelta(hours=1)
COMPONENT_REPO = "https://github.com/danielnguyen/home-assistant-york-coronavirus/"

# Configure and add devices
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensors = []
    for municipality in config[CONF_MUNICIPALITIES]:
        for case_type in CASE_TYPES:
            sensors.append(YorkCoronavirusSensor(hass, municipality, case_type))
    async_add_entities(sensors, True)

class YorkCoronavirusSensor(Entity):

    def __init__(self, hass, municipality: str, case_type: str):
        """Initialize the sensor."""
        self._state =  {}
        self._name = f"York Region Coronavirus {case_type}"
        self.hass = hass
        self.municipality = municipality
        self.case_type = case_type
    
    @property
    def icon(self):
        """Return the icon."""
        return CASE_TYPES[self.case_type]

    @property
    def name(self):
        """Return the name."""
        return self._name
    
    @property
    def state(self):
        """Return the state."""
        return self._state
    
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "people"

    async def async_update(self):
        """Update the sensor."""
        await update_data(self.hass)
        updated_data = self.hass.data[DOMAIN_DATA][self.municipality].get(self.case_type)
        if updated_data is None:
            updated_data = self._state
        else:
            self._state = updated_data