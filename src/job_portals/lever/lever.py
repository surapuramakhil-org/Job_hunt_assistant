import re
from src.job_portals.base_job_portal import BaseJobPortal
from src.job_portals.lever.authenticator import LeverAuthenticator
from src.job_portals.lever.jobs_page import SearchLeverJobs
from src.job_portals.lever.application_page import LeverApplicationPage
from src.job_portals.lever.job_page import LeverJobPage

class Lever(BaseJobPortal):

    def __init__(self, driver, work_preferences):
        self.driver = driver
        self._authenticator = LeverAuthenticator(driver)
        self._jobs_page = SearchLeverJobs(driver, work_preferences)
        self._application_page = LeverApplicationPage(driver)
        self._job_page = LeverJobPage(driver)
    
    @property
    def jobs_page(self):
        return self._jobs_page

    @property
    def job_page(self):
        return self._job_page

    @property
    def authenticator(self):
        return self._authenticator

    @property
    def application_page(self):
        return self._application_page