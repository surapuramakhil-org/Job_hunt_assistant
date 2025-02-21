import time
import traceback
from typing import List, Text
from regex import E
from selenium.webdriver.remote.webelement import WebElement
from custom_exception import JobSkipException
from logger import logger
from job_portals.application_form_elements import (
    SelectQuestion,
    SelectQuestionType,
    TextBoxQuestion,
    TextBoxQuestionType,
)
from job_portals.base_job_portal import BaseApplicationPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils import browser_utils


class LeverApplicationPage(BaseApplicationPage):

    def __init__(self, driver):
        super().__init__(driver)

    def save(self) -> None:
        raise NotImplementedError

    def discard(self) -> None:
        raise NotImplementedError
    
    def wait_until_ready(self):
        try:
            WebDriverWait(self.driver, 120).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//div[@class='loading-indicator']")
                )
            )
        except TimeoutException as e:
            logger.error(f"Loading indicator did not disappear within timeout: {str(e)}")
            raise JobSkipException("Page load timeout - loading indicator remained visible")
        except Exception as e:
            logger.error(f"Error occurred while waiting for page to load: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Error occurred while waiting for page to load {e} {traceback.format_exc()}")

    def click_submit_button(self) -> None:
        try:
            submit_button = self.driver.find_element(By.ID, "btn-submit")
            submit_button.click()
            
        except NoSuchElementException:
            logger.error("Submit button not found.")
            raise JobSkipException("Submit button not found.")
        
        except ElementClickInterceptedException as e:
            logger.warning("submit button has been intercepted / interrupted, solve checks & submit application then do keyborad interrupt")
            browser_utils.security_check(self.driver)
        except Exception as e:

            logger.error(
                f"Error occurred while clicking submit button: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while clicking submit button {e} {traceback.format_exc()}"
            )

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
            logger.error(
                f"Error occurred while checking for submit button: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while checking for submit button {e} {traceback.format_exc()}"
            )

    def get_file_upload_elements(self):
        raise NotImplementedError

    def upload_file(self, element: WebElement, file_path: str) -> None:
        try:
            file_input = element.find_element(By.XPATH, ".//input[@type='file']")
            file_input.send_keys(file_path)
        except Exception as e:
            logger.error(
                f"Error occurred while uploading file: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while uploading file {e} {traceback.format_exc()}"
            )

    def get_form_sections(self) -> List[WebElement]:
        try:
            form_sections = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'section') and contains(@class, 'application-form') and contains(@class, 'page-centered')]",
            )
            return form_sections
        except Exception as e:
            logger.error(
                f"Error occurred while getting form sections: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while getting form sections {e} {traceback.format_exc()}"
            )

    def accept_terms_of_service(self, element: WebElement) -> None:
        raise NotImplementedError

    def is_terms_of_service(self, element: WebElement) -> bool:
        return False

    def is_radio_question(self, element: WebElement) -> bool:
        try:
            element.find_element(By.XPATH, ".//input[@type='checkbox']")
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.error(
                f"Error occurred while checking if element is a radio question: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while checking if element is a radio question {e} {traceback.format_exc()}"
            )

    def web_element_to_radio_question(self, element: WebElement) -> SelectQuestion:
        try:
            # Extract question text from application-label div
            question_label = element.find_element(
                By.XPATH, ".//div[contains(@class, 'application-label')]"
            ).text.strip()

            # Find all radio/checkbox input elements
            inputs = element.find_elements(
                By.XPATH, ".//input[@type='radio' or @type='checkbox']"
            )

            # Collect non-empty option values
            options = []
            for input_elem in inputs:
                value = input_elem.get_attribute("value")
                if value and value not in options:  # Prevent duplicates
                    options.append(value)

            # Determine question type based on input types
            question_type = SelectQuestionType.MULTI_SELECT if any(
                input_elem.get_attribute("type") == "checkbox" for input_elem in inputs
            ) else SelectQuestionType.SINGLE_SELECT

            # Check for required status using description text
            required = True
            description_elements = element.find_elements(
                By.XPATH, ".//p[contains(@class, 'description')]"
            )
            for desc in description_elements:
                if "(Optional)" in desc.text:
                    required = False
                    break

            return SelectQuestion(
                question=question_label,
                options=options,
                type=question_type,
                required=required
            )
            
        except Exception as e:
            logger.error(
                f"Error converting element to radio question: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error converting element to radio question: {e} {traceback.format_exc()}"
            )


    def select_radio_option(
        self, radio_question_web_element: WebElement, answer: str
    ) -> None:
        try:
            radio_input = radio_question_web_element.find_element(
                By.XPATH, f".//input[@value='{answer}']"
            )
            radio_input.click()
        except Exception as e:
            logger.error(
                f"Error occurred while selecting radio option: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while selecting radio option {e} {traceback.format_exc()}"
            )
        raise NotImplementedError

    def is_textbox_question(self, element: WebElement) -> bool:
        try:
            if element.find_elements(By.XPATH, ".//textarea"):
                return True
                
            input_element = element.find_element(
                By.XPATH, ".//input[@type='text' or @type='number']"
            )
            return input_element.is_displayed() and input_element.is_enabled()
            
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.error(f"Textbox check error: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Textbox verification failed: {e}")

    def web_element_to_textbox_question(self, element: WebElement) -> TextBoxQuestion:
        try:
            # Extract the question text from the label div
            question_label = element.find_element(
                By.XPATH, ".//div[contains(@class, 'application-label')]"
            ).text

            # Locate the input element (type can be 'text', 'number', or 'textarea')
            input_element = element.find_element(
                By.XPATH, ".//input[@type='text' or @type='number'] | .//textarea"
            )

            # Determine the type of input field
            input_type = input_element.tag_name if input_element.tag_name == "textarea" else input_element.get_attribute("type")

            if input_type == "text" or input_type == "textarea":
                question_type = TextBoxQuestionType.TEXT
            elif input_type == "number":
                question_type = TextBoxQuestionType.NUMERIC
            else:
                raise ValueError(f"Unsupported input type: {input_type}")

            is_required = bool(
                element.find_elements(By.XPATH, ".//span[@class='required']")
            )

            return TextBoxQuestion(
                question=question_label, type=question_type, required=is_required
            )
        except Exception as e:
            logger.error(
                f"Error occurred while converting element to textbox question: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while converting element to textbox question {e} {traceback.format_exc()}"
            )

    def fill_textbox_question(self, element: WebElement, answer: str) -> None:
        """Handles text input fields with special handling for location inputs"""
        try:
            if self._is_location_input(element):
                self._handle_location_input(element, answer)
                return

            input_element = element.find_element(By.XPATH, ".//textarea | .//input[@type='text' or @type='number']")
            input_element.clear()
            input_element.send_keys(answer)

        except Exception as e:
            logger.error(f"Input handling failed: {e} {traceback.format_exc()}")
            raise JobSkipException(f"Text input error: {str(e)}")

    def _is_location_input(self, element: WebElement) -> bool:
        """Check if the element contains a location input field"""
        return len(element.find_elements(
            By.CSS_SELECTOR, "input.location-input[data-qa='location-input']"
        )) > 0

    def _handle_location_input(self, element: WebElement, answer: str) -> None:
        """Specialized handler for location autocomplete inputs"""
        input_element = element.find_element(
            By.CSS_SELECTOR, "input.location-input[data-qa='location-input']"
        )
        
        # Clear existing input
        input_element.send_keys(Keys.CONTROL + "a")
        input_element.send_keys(Keys.DELETE)
        
        # Type answer to trigger suggestions
        for char in answer:
            input_element.send_keys(char)
            time.sleep(0.1)
        
        # Handle dropdown interaction
        try:
            dropdown = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "div.dropdown-container")
                )
            )
            first_result = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div.dropdown-results > div:first-child")
                )
            )
            first_result.click()
        except TimeoutException:
            if "No location found" in element.text:
                raise JobSkipException("Invalid location entered")
            raise
        
        # Verify selection
        hidden_value = element.find_element(
            By.CSS_SELECTOR, "input#selected-location"
        ).get_attribute("value")
        
        if not hidden_value:
            raise ValueError("Location selection validation failed")

    def is_date_question(self, element: WebElement) -> bool:
        return False

    def has_next_button(self) -> bool:
        return False

    def click_next_button(self) -> None:
        raise NotImplementedError

    def has_errors(self) -> None:
        raise NotImplementedError

    def check_for_errors(self) -> None:
        raise NotImplementedError

    def get_input_elements(self, form_section: WebElement) -> List[WebElement]:
        try:
            input_elements = form_section.find_elements(By.XPATH, ".//ul/li[contains(@class, 'application-question')]")

            if not input_elements:
                input_elements = form_section.find_elements(
                    By.XPATH, ".//textarea | .//input"
                )

            return input_elements
        except Exception as e:
            logger.error(
                f"Error occurred while getting input elements: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while getting input elements {e} {traceback.format_exc()}"
            )

    def is_upload_field(self, element: WebElement) -> bool:
        try:
            element.find_element(By.XPATH, ".//input[@type='file']")
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.error(
                f"Error occurred while checking for upload field: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while checking for upload field {e} {traceback.format_exc()}"
            )

    def get_upload_element_heading(self, element: WebElement) -> str:
        try:
            heading = element.find_element(
                By.XPATH, ".//div[contains(@class, 'application-label')]"
            ).text
            return heading
        except Exception as e:
            logger.error(
                f"Error occurred while getting upload element heading: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while getting upload element heading {e} {traceback.format_exc()}"
            )

    def is_dropdown_question(self, element: WebElement) -> bool:
        try:
            element.find_element(By.XPATH, ".//select")
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.error(
                f"Error occurred while checking for dropdown question: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while checking for dropdown question {e} {traceback.format_exc()}"
            )

    def web_element_to_dropdown_question(self, element: WebElement) -> SelectQuestion:
        try:
            # Extract the question text from the label div
            question_label = element.find_element(
                By.XPATH, ".//div[@class='application-label']"
            ).text

            # Locate the select element
            select_element = element.find_element(By.XPATH, ".//select")

            # Extract all options from the select element
            options = [
                option.text
                for option in select_element.find_elements(By.TAG_NAME, "option")
            ]

            is_required = bool(
                element.find_elements(By.XPATH, ".//span[@class='required']")
            )

            # Determine the type of select element

            select_type = select_element.get_attribute("multiple")
            if select_type:
                question_type = SelectQuestionType.MULTI_SELECT
            else:
                question_type = SelectQuestionType.SINGLE_SELECT

            return SelectQuestion(
                question=question_label,
                options=options,
                required=is_required,
                type=question_type,
            )

        except Exception as e:
            logger.error(
                f"Error occurred while converting element to dropdown question: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while converting element to dropdown question {e} {traceback.format_exc()}"
            )

    def select_dropdown_option(self, element: WebElement, answer: str) -> None:
        try:
            select_element = element.find_element(By.XPATH, ".//select")
            for option in select_element.find_elements(By.TAG_NAME, "option"):
                if option.text == answer:
                    option.click()
                    return
            raise ValueError(f"Option '{answer}' not found in dropdown")
        except Exception as e:
            logger.error(
                f"Error occurred while selecting dropdown option: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while selecting dropdown option {e} {traceback.format_exc()}"
            )
