import unittest
from unittest.mock import MagicMock, patch
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from ai_hawk.job_applier import AIHawkJobApplier
from job_portals.lever.application_page import LeverApplicationPage
from job_portals.base_job_portal import BaseJobPortal
from job import Job
from ai_hawk.llm.llm_manager import GPTAnswerer
from job_application_saver import ApplicationSaver
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from job_portals.lever.job_page import LeverJobPage
from main import init_browser
from utils import browser_utils
class TestLeverJobPortalIntegration(unittest.TestCase):
    
    def setUp(self):
        self.driver = init_browser()
        browser_utils.set_default_driver(self.driver)

        # Mock dependencies
        self.mock_job_page = LeverJobPage(self.driver)
        self.mock_application_page = LeverApplicationPage(self.driver)
        self.mock_job_portal = MagicMock(spec=BaseJobPortal)
        self.mock_job_portal.application_page = self.mock_application_page
        self.mock_job_portal.job_page = self.mock_job_page

        self.mock_gpt_answerer = MagicMock(spec=GPTAnswerer)
        self.mock_gpt_answerer.answer_question_from_options.side_effect = lambda question, options: options[0]
        self.mock_gpt_answerer.answer_question_textual_wide_range.side_effect = lambda question: "Sample answer"
        self.mock_gpt_answerer.answer_question_numeric.side_effect = lambda question: "12345"
        self.mock_gpt_answerer.is_job_suitable.return_value = (True, 0.9, "Suitable job")
        self.mock_resume_generator_manager = MagicMock()
        self.mock_work_preferences = {"keywords_whitelist": []}

        # Initialize AIHawkJobApplier with mocks
        self.job_applier = AIHawkJobApplier(
            job_portal=self.mock_job_portal,
            resume_dir=None,
            set_old_answers=[],
            gpt_answerer=self.mock_gpt_answerer,
            work_preferences=self.mock_work_preferences,
            resume_generator_manager=self.mock_resume_generator_manager,
        )

    def tearDown(self):
        # Quit the WebDriver
        self.driver.quit()

    def get_job_url(self, relative_path: str) -> str:
        from pathlib import Path
        path = Path(relative_path).resolve()
        return path.as_uri()
        

    @patch.object(ApplicationSaver, 'save')
    def test_lever_apply_to_job_success(self, mock_save):
        
        # Mock job object
        self.mock_job = Job(
            title="Software Engineer",
            company="Tech Company",
            description="Looking for a Python developer with Django experience.",
            link=self.get_job_url("tests/resources/lever_application_pages/job1/https-:jobs.lever.co:nielsen:f221a3f5-4045-49f0-a443-62b0030dc56f.html")
        )

        print(f"Testing Lever job {self.mock_job.link} ")

        # Mock the click on the apply button
        self.mock_job_page.click_apply_button = MagicMock()
        self.mock_job_page.click_apply_button.side_effect = lambda: self.driver.get(self.get_job_url("tests/resources/lever_application_pages/job1/https-:jobs.lever.co:nielsen:f221a3f5-4045-49f0-a443-62b0030dc56f:apply.html"))
        self.mock_job_page.click_apply_button()

        try:
            self.job_applier.apply_to_job(self.mock_job)
        except Exception as e:
            self.fail(f"apply_to_job raised an exception: {e}")
        
        self.mock_gpt_answerer.is_job_suitable.assert_called_once()
        mock_save.assert_called_once()

        self.mock_gpt_answerer.is_job_suitable.assert_called_once()
        mock_save.assert_called_once()