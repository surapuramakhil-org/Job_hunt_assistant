import traceback
from typing import List, Text
from regex import E
from selenium.webdriver.remote.webelement import WebElement
from custom_exception import JobSkipException
from logger import logger
from src.job_portals.application_form_elements import (
    SelectQuestion,
    SelectQuestionType,
    TextBoxQuestion,
    TextBoxQuestionType,
)
from src.job_portals.base_job_portal import BaseApplicationPage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class LeverApplicationPage(BaseApplicationPage):
    def save(self) -> None:
        raise NotImplementedError

    def discard(self) -> None:
        raise NotImplementedError

    def click_submit_button(self) -> None:
        try:
            submit_button = self.driver.find_element(By.ID, "btn-submit")
            submit_button.click()
            
        except NoSuchElementException:
            logger.error("Submit button not found.")
            raise JobSkipException("Submit button not found.")
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
        return False

    def web_element_to_radio_question(self, element: WebElement):
        raise NotImplementedError

    def select_radio_option(
        self, radio_question_web_element: WebElement, answer: str
    ) -> None:
        raise NotImplementedError

    def is_textbox_question(self, element: WebElement) -> bool:
        try:
            input_element = element.find_element(
                By.XPATH, ".//input[@type='text' or @type='number']"
            )
            return input_element.is_displayed() and input_element.is_enabled()
        except NoSuchElementException:
            return False
        except Exception as e:
            logger.error(
                f"Error occurred while checking if element is a textbox question: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while checking if element is a textbox question {e} {traceback.format_exc()}"
            )

    def web_element_to_textbox_question(self, element: WebElement) -> TextBoxQuestion:
        try:
            # Extract the question text from the label div
            question_label = element.find_element(
                By.XPATH, ".//div[@class='application-label']"
            ).text

            # Locate the input element (type can be 'text' or 'number')
            input_element = element.find_element(
                By.XPATH, ".//input[@type='text' or @type='number']"
            )

            # Determine the type of input field
            input_type = input_element.get_attribute("type")

            is_required = bool(
                element.find_elements(By.XPATH, ".//span[@class='required']")
            )

            if input_type == "text":
                question_type = TextBoxQuestionType.TEXTBOX
            elif input_type == "number":
                question_type = TextBoxQuestionType.NUMERIC
            else:
                raise ValueError(f"Unsupported input type: {input_type}")

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
        try:
            input_element = element.find_element(
                By.XPATH, ".//input[@type='text' or @type='number']"
            )
            input_element.send_keys(answer)
        except Exception as e:
            logger.error(
                f"Error occurred while filling textbox question: {e} {traceback.format_exc()}"
            )
            raise JobSkipException(
                f"Error occurred while filling textbox question {e} {traceback.format_exc()}"
            )

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
            input_elements = form_section.find_elements(By.XPATH, ".//ul/li")

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
