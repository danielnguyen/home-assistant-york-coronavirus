"""
A component which pulls down the daily Toronto Public Health COVID-19 updates.
For more details about this component, please refer to the documentation at
https://github.com/danielnguyen/home-assistant-toronto-covid19
"""
import datetime
import logging

from datetime import timedelta
from dateutil import parser

from homeassistant.helpers.entity import Entity
from . import update_data
from .const import DOMAIN_DATA
from .const import VERSION
from .toronto_coronavirus import get_cases

__version__ = VERSION
_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "all": "mdi:hospital-box",
    "active": "mdi:emoticon-sad-outline",
    "recovered": "mdi:emoticon-happy-outline",
    "deaths": "mdi:emoticon-cry-outline"
}

DEFAULT_SCAN_INTERVAL = timedelta(hours=1)
SCAN_INTERVAL = timedelta(hours=1)
COMPONENT_REPO = "https://github.com/danielnguyen/home-assistant-toronto-covid19/"

# Configure and add devices
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensors = []
    for (k, v) in SENSORS.items():
        sensors.append(TorontoCoronavirusSensor(hass, k))
    async_add_entities(sensors, True)

class TorontoCoronavirusSensor(Entity):

    def __init__(self, hass, case_type: str):
        """Initialize the sensor."""
        self._attr =  {}
        self._name = f"Toronto Coronavirus {case_type}"
        self.hass = hass
        self.case_type = case_type
    
    @property
    def icon(self):
        """Return the icon."""
        return SENSORS[self.case_type]

    @property
    def name(self):
        """Return the name."""
        return self._name
    
    @property
    def state(self):
        """Return the state."""
        return self._attr
    
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "people"

    async def async_update(self):
        """Update the sensor."""
        await update_data(self.hass)
        updated_data = self.hass.data[DOMAIN_DATA].get(self.case_type)
        if updated_data is None:
            updated_data = self._attr
        else:
            self._attr = updated_data