from operator import is_
from logger import logger
import os
import json
import shutil

from dataclasses import asdict

from config import JOB_APPLICATIONS_DIR
from job_application import JobApplication


def get_base_dir():
    return JOB_APPLICATIONS_DIR


class ApplicationSaver:

    def __init__(self, job_application: JobApplication):
        self.job_application = job_application
        self.job_application_files_path = None

    # Function to create a directory for each job application
    def create_application_directory(self, is_failed: bool):
        job = self.job_application.job

        # Create a unique directory name using the application ID and company name
        dir_name = f"{job.id} - {job.company} {job.title}"

        base_dir = get_base_dir()

        if is_failed:
            base_dir = os.path.abspath(base_dir)
            base_dir_parts = base_dir.split(os.sep)
            base_dir_parts[-1] = f"failed_{base_dir_parts[-1]}"
            base_dir = os.sep.join(base_dir_parts)

        dir_path = os.path.join(base_dir, dir_name)

        # Create the directory if it doesn't exist
        os.makedirs(dir_path, exist_ok=True)
        self.job_application_files_path = dir_path
        return dir_path

    # Function to save the job application details and job description as JSON files
    def _save(self):

        if self.job_application_files_path is None:
            raise ValueError(
                "Job application file path is not set. Please create the application directory first."
            )

        # Save job application details
        application_json_file_path = os.path.join(
            self.job_application_files_path, "job_application.json"
        )
        with open(application_json_file_path, "w") as json_file:
            json.dump((self.job_application.to_json()), json_file, indent=4)

    # Function to save files like Resume and CV
    def save_file(self, dir_path, file_path, new_filename):
        if dir_path is None:
            raise ValueError("dir path cannot be None")

        # Copy the file to the application directory with a new name
        destination = os.path.join(dir_path, new_filename)
        shutil.copy(file_path, destination)

    @staticmethod
    def save(job_application: JobApplication, is_failed: bool = False):

        saver = ApplicationSaver(job_application)
        saver.create_application_directory(is_failed)
        saver._save()
        # todo: tempory fix, to rely on resume and cv path from job object instead of job application object
        if job_application.resume_path:
            saver.save_file(
                saver.job_application_files_path,
                job_application.job.resume_path,
                "resume.pdf",
            )
        logger.debug(
            f"Saving cover letter to path: {job_application.cover_letter_path}"
        )
        if job_application.cover_letter_path:
            saver.save_file(
                saver.job_application_files_path,
                job_application.job.cover_letter_path,
                "cover_letter.pdf",
            )
