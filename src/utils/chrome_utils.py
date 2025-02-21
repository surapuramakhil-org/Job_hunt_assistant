import os
from loguru import logger
from selenium import webdriver
import undetected_chromedriver as uc

chromeProfilePath = os.path.join(os.getcwd(), "chrome_profile", "linkedin_profile")

def ensure_chrome_profile():
    logger.debug(f"Ensuring Chrome profile exists at path: {chromeProfilePath}")
    profile_dir = os.path.dirname(chromeProfilePath)
    if not os.path.exists(profile_dir):
        os.makedirs(profile_dir)
        logger.debug(f"Created directory for Chrome profile: {profile_dir}")
    if not os.path.exists(chromeProfilePath):
        os.makedirs(chromeProfilePath)
        logger.debug(f"Created Chrome profile directory: {chromeProfilePath}")
    return chromeProfilePath

def chrome_browser_options():
    logger.debug("Setting Chrome browser options")
    ensure_chrome_profile()
    options = uc.ChromeOptions()
    
    # Essential arguments only
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Profile configuration
    if chromeProfilePath:
        options.add_argument(f'--user-data-dir={os.path.dirname(chromeProfilePath)}')
        options.add_argument(f'--profile-directory={os.path.basename(chromeProfilePath)}')
    else:
        options.add_argument("--incognito")
    
    return options


