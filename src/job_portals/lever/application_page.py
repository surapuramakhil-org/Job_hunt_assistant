import traceback
from typing import List
from regex import E
from selenium.webdriver.remote.webelement import WebElement
from custom_exception import JobSkipException
from logger import logger
from src.job_portals.application_form_elements import SelectQuestion
from src.job_portals.base_job_portal import BaseApplicationPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class LeverApplicationPage(BaseApplicationPage):
    def save(self) -> None:
        raise NotImplementedError

    def discard(self) -> None:
        raise NotImplementedError

    def click_submit_button(self) -> None:
        raise NotImplementedError

    def handle_errors(self) -> None:
        raise NotImplementedError

    def has_submit_button(self) -> bool:
        try:
            # Attempt to locate the submit button by its ID
            self.driver.find_element(By.ID, "btn-submit")
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.error(f"Error occurred while checking for submit button: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Error occurred while checking for submit button {e} {traceback.format_exc()}")

    def get_file_upload_elements(self):
        raise NotImplementedError

    def upload_file(self, element, file_path: str) -> None:
        try:
            file_input = element.find_element(By.XPATH, ".//input[@type='file']")
            file_input.send_keys(file_path)
        except Exception as e:
            logger.error(f"Error occurred while uploading file: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Error occurred while uploading file {e} {traceback.format_exc()}")

    def get_form_sections(self) -> List[WebElement]:
        try:
            form_sections = self.driver.find_elements(
                By.XPATH, 
                "//div[contains(@class, 'section') and contains(@class, 'application-form') and contains(@class, 'page-centered')]"
            )
            return form_sections
        except Exception as e:
            logger.error(f"Error occurred while getting form sections: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Error occurred while getting form sections {e} {traceback.format_exc()}")

    def accept_terms_of_service(self, section) -> None:
        raise NotImplementedError

    def is_terms_of_service(self, section) -> bool:
        return False

    def is_radio_question(self, section) -> bool:
        raise NotImplementedError

    def web_element_to_radio_question(self, section):
        raise NotImplementedError

    def select_radio_option(self, radio_question_web_element, answer: str) -> None:
        raise NotImplementedError

    def is_textbox_question(self, section) -> bool:
        raise NotImplementedError

    def web_element_to_textbox_question(self, section):
        raise NotImplementedError

    def fill_textbox_question(self, section, answer: str) -> None:
        raise NotImplementedError

    def is_date_question(self, section) -> bool:
        raise NotImplementedError

    def has_next_button(self) -> bool:
        return False

    def click_next_button(self) -> None:
        raise NotImplementedError

    def has_errors(self) -> None:
        raise NotImplementedError

    def check_for_errors(self) -> None:
        raise NotImplementedError

    def get_input_elements(self, form_section : WebElement) -> List[WebElement]:
        try:
            input_elements = form_section.find_elements(By.XPATH, ".//ul/li")

            if not input_elements:
                input_elements = form_section.find_elements(By.XPATH, ".//textarea | .//input")

            return input_elements
        except Exception as e:
            logger.error(f"Error occurred while getting input elements: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Error occurred while getting input elements {e} {traceback.format_exc()}")

    def is_upload_field(self, element: WebElement) -> bool:
        try:
            element.find_element(By.XPATH, ".//input[@type='file']")
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.error(f"Error occurred while checking for upload field: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Error occurred while checking for upload field {e} {traceback.format_exc()}")
            
    def get_upload_element_heading(self, element: WebElement) -> str:
        try:
            heading = element.find_element(By.XPATH, ".//div[contains(@class, 'application-label')]").text
            return heading
        except Exception as e:
            logger.error(f"Error occurred while getting upload element heading: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Error occurred while getting upload element heading {e} {traceback.format_exc()}")

    def is_dropdown_question(self, section: WebElement) -> bool:
        raise NotImplementedError

    def web_element_to_dropdown_question(self, section: WebElement) -> SelectQuestion:
        raise NotImplementedError

    def select_dropdown_option(self, section: WebElement, answer: str) -> None:
        raise NotImplementedError

