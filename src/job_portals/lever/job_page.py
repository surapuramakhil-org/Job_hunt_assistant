import traceback
from loguru import logger
from custom_exception import JobNotSuitableException, JobSkipException
from src.job_portals.base_job_portal import BaseJobPage
from selenium.webdriver.common.by import By

from utils import time_utils


class LeverJobPage(BaseJobPage):

    def __init__(self, driver):
        super().__init__(driver)

    def goto_job_page(self, job):
        try:
            self.driver.get(job.link)
            logger.debug(f"Navigated to job link: {job.link}")
        except Exception as e:
            logger.error(f"Failed to navigate to job link: {job.link}, error: {str(e)}")
            raise e

    def get_apply_button(self, job_context):
        raise NotImplementedError

    def check_for_premium_redirect(self, job, max_attempts=3):
        raise NotImplementedError

    def click_apply_button(self, job_context) -> None:
        try:
            apply_button = self.driver.find_element(
                By.XPATH,
                "//a[contains(@class, 'postings-btn') and contains(@class, 'template-btn-submit')]"
            )
            apply_button.click()
        except Exception as e:
            logger.error(f"Failed to click apply button: {e}, { traceback.format_exc()}")
            raise JobSkipException("Failed to click apply button")

    def _find_easy_apply_button(self, job_context):
        raise NotImplementedError

    def _scroll_page(self) -> None:
        raise NotImplementedError

    def get_job_description(self, job) -> str:
        try:
            job_description_element = self.driver.find_element(
                By.XPATH,
                "//div[@class='section-wrapper page-full-width']",
            )
            job_description = job_description_element.text
            return job_description
        except Exception as e:
            logger.error(
                f"Error getting job description: {e} , { traceback.format_exc()}"
            )
            return ""

    def get_recruiter_link(self) -> str:
        return ""
