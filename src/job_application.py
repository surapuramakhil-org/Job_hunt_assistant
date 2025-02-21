from attr import asdict
from job import Job
import json


class JobApplication:

    def __init__(self, job: Job):
        self.job = job
        # contains only question -> added when discovered
        self.empty_form = []
        # contains question and answer -> added when answered
        self.application_form = []

    def add_question_to_form(self, question: str):
        self.empty_form.append(question)

    def save_application_data(self, application_question: dict):
        self.application_form.append(application_question)

    def to_json(self):
        return {
            'job': self.job.__dict__,
            'resume_path': self.resume_path,
            'cover_letter_path': self.cover_letter_path,
            'empty_form': self.empty_form,
            'application_form': self.application_form
        }
    
    @property
    def resume_path(self):
        return self.job.resume_path

    @resume_path.setter
    def resume_path(self, path: str):
        self.job.resume_path = path

    @property
    def cover_letter_path(self):
        return self.job.cover_letter_path

    @cover_letter_path.setter
    def cover_letter_path(self, path: str):
        self.job.cover_letter_path = path
