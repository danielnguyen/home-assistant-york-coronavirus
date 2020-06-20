import os
import logging
import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers import discovery

from .const import CONF_MUNICIPALITIES, DOMAIN, DOMAIN_DATA, ISSUE_URL, PLATFORMS, REQUIRED_FILES, STARTUP, VERSION
from .york_coronavirus import get_cases
from .york_coronavirus import get_all_municipalities

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_MUNICIPALITIES): vol.All(cv.ensure_list, [cv.string]),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

async def async_setup(hass, config):
    """Set up this component."""

    # Print startup message
    startup = STARTUP.format(name=DOMAIN, version=VERSION, issueurl=ISSUE_URL)
    _LOGGER.info(startup)

    # Check that all required files are present
    file_check = await check_files(hass)
    if not file_check:
        return False

    # Create DATA dict
    hass.data[DOMAIN_DATA] = {}

    # Load platforms
    for platform in PLATFORMS:
        hass.async_create_task(
            discovery.async_load_platform(hass, platform, DOMAIN, {}, config))
    return True


async def update_data(hass):
    """Update data."""

    municipalities = []
    config = hass.config[DOMAIN]

    if len(config[CONF_MUNICIPALITIES]) < 1:
        municipalities = get_all_municipalities()
    else:
        for municipality in config[CONF_MUNICIPALITIES]:
            municipalities.append(municipality)

    cases_by_municipality = {}
    try:
        for municipality in municipalities:
            cases_by_municipality[municipality] = get_cases(municipality)
        hass.data[DOMAIN_DATA] = cases_by_municipality
    except Exception as error:  # pylint: disable=broad-except
        _LOGGER.error("Could not update data - %s", error)


async def check_files(hass):
    """Retrun bool that idicate that all files are present."""
    base = "{}/custom_components/{}/".format(hass.config.path(), DOMAIN)
    missing = []
    for file in REQUIRED_FILES:
        fullpath = "{}{}".format(base, file)
        if not os.path.exists(fullpath):
            missing.append(file)

    if missing:
        _LOGGER.critical("The following files are missing: %s", str(missing))
        returnvalue = False
    else:
        returnvalue = True

    return returnvalue