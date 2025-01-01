# In this file, you can set the configurations of the app.
import os
from dotenv import load_dotenv
from constants import BING, BRAVE, DEBUG, GOOGLE

load_dotenv()

#config related to logging must have prefix LOG_
LOG_LEVEL = DEBUG
LOG_SELENIUM_LEVEL = DEBUG
LOG_TO_FILE = True
LOG_TO_CONSOLE = True

MINIMUM_WAIT_TIME_IN_SECONDS = 60

JOB_APPLICATIONS_DIR = "job_applications"
JOB_SUITABILITY_SCORE = 7

JOB_MAX_APPLICATIONS = 5
JOB_MIN_APPLICATIONS = 1

LLM_MODEL_TYPE = 'openai'
LLM_MODEL = 'gpt-4o-mini'
# Only required for OLLAMA models
LLM_API_URL = ''

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", None)
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", None)
BING_API_KEY = os.getenv("BING_API_KEY", None)
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", None)

ALLOWED_SEARCH_ENGINES = [GOOGLE]
DEFAULT_SEARCH_ENGINE = GOOGLE

def validate_config():
    """
    Validate that all required API keys and configurations are set.
    Raises an exception if any critical configuration is missing.
    """
    missing_keys = []

    if ALLOWED_SEARCH_ENGINES == []:
        missing_keys.append("ALLOWED_SEARCH_ENGINES can be an empty list")
    
    if GOOGLE in ALLOWED_SEARCH_ENGINES and (not GOOGLE_API_KEY or not GOOGLE_SEARCH_ENGINE_ID):
        missing_keys.append("GOOGLE_API_KEY or GOOGLE_SEARCH_ENGINE_ID")
    
    if BING in ALLOWED_SEARCH_ENGINES and not BING_API_KEY:
        missing_keys.append("BING_API_KEY")
    
    if BRAVE in ALLOWED_SEARCH_ENGINES and not BRAVE_API_KEY:
        missing_keys.append("BRAVE_API_KEY")

    if missing_keys:
        raise EnvironmentError(
            f"Missing required configuration(s): {', '.join(missing_keys)}. "
            "Please set these as environment variables."
        )

print(f'ENV: {os.getenv("ENV")}')

# Run validation on import
if not os.getenv('ENV') == 'test':
    validate_config()