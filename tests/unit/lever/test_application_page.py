import os
from selenium.webdriver.common.by import By
import pytest
from job_portals.lever.application_page import LeverApplicationPage
from main import init_browser

@pytest.fixture
def lever_application_page():
    driver = init_browser()
    driver.get("file:///" + os.path.abspath("tests/unit/resources/lever_application_pages/Nielsen - Senior Software Engineer - Bigdata ( Java _ Scala _ Python , Spark, SQL , AWS).html"))
    return LeverApplicationPage(driver)

def test_click_submit_button(lever_application_page):
    lever_application_page.click_submit_button()
    # Verify success through error checking
    assert lever_application_page.has_errors() is False

def test_has_submit_button(lever_application_page):
    assert lever_application_page.has_submit_button()

def test_upload_file(lever_application_page, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    upload_element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='file']")
    lever_application_page.upload_file(upload_element, str(test_file))
    assert "test.txt" in lever_application_page.driver.page_source

def test_get_form_sections(lever_application_page):
    sections = lever_application_page.get_form_sections()
    assert len(sections) > 0

def test_is_radio_question(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='checkbox']")
    assert lever_application_page.is_radio_question(element)

def test_web_element_to_radio_question(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='checkbox']")
    question = lever_application_page.web_element_to_radio_question(element)
    assert question.options != []

def test_select_radio_option(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='checkbox']")
    lever_application_page.select_radio_option(element, "option_value")
    assert element.is_selected()

def test_is_textbox_question(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='text']")
    assert lever_application_page.is_textbox_question(element)

def test_web_element_to_textbox_question(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='text']")
    question = lever_application_page.web_element_to_textbox_question(element)
    assert question.required in [True, False]

def test_fill_textbox_question(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='text']")
    lever_application_page.fill_textbox_question(element, "test")
    assert element.get_attribute("value") == "test"

def test_get_input_elements(lever_application_page):
    sections = lever_application_page.get_form_sections()
    inputs = lever_application_page.get_input_elements(sections[0])
    assert len(inputs) > 0

def test_is_upload_field(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='file']")
    assert lever_application_page.is_upload_field(element)

def test_get_upload_element_heading(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//input[@type='file']")
    heading = lever_application_page.get_upload_element_heading(element)
    assert "resume" in heading.lower()

def test_is_dropdown_question(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//select")
    assert lever_application_page.is_dropdown_question(element)

def test_web_element_to_dropdown_question(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//select")
    question = lever_application_page.web_element_to_dropdown_question(element)
    assert len(question.options) > 0

def test_select_dropdown_option(lever_application_page):
    element = lever_application_page.driver.find_element(By.XPATH, "//select")
    lever_application_page.select_dropdown_option(element, "option_value")
    selected = element.find_element(By.XPATH, ".//option[@selected]")
    assert selected.text == "option_value"
