"""
Integration tests for ApplicationSaver.save() method
Verifies file system operations and output compliance
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch
from job import Job
from job_application import JobApplication
from job_application_saver import ApplicationSaver

@pytest.fixture
def sample_job(tmp_path):
    """Fixture creating a Job instance with test files"""
    resume = tmp_path / "resume.pdf"
    resume.write_text("Dummy resume content")
    
    cover = tmp_path / "cover.pdf" 
    cover.write_text("Dummy cover letter")
    
    return Job(
        id="PYDEV-2025",
        title="Senior Python Developer",
        company="Code Masters Inc",
        portal="LinkedIn",
        resume_path=str(resume),
        cover_letter_path=str(cover),
        description="Develop high-quality Python applications",
    )

@pytest.fixture
def job_application(sample_job):
    """Fixture creating a populated JobApplication"""
    app = JobApplication(sample_job)
    app.add_question_to_form("Availability")
    app.save_application_data({
        "question": "Experience", 
        "answer": "10+ years Python"
    })
    return app

class TestApplicationSaverIntegration:
    """Integration test suite for file system operations"""
    
    def test_normal_save_creates_correct_structure(self, tmp_path, job_application):
        """Verify directory structure and file creation for successful saves"""
        with patch('job_application_saver.get_base_dir', return_value=str(tmp_path)):
            ApplicationSaver.save(job_application)
            
        expected_dir = tmp_path / "PYDEV-2025 - Code Masters Inc Senior Python Developer"
        assert expected_dir.exists(), "Main directory not created"
        
        # Verify required files
        assert (expected_dir / "job_application.json").exists()
        assert (expected_dir / "resume.pdf").exists()
        assert (expected_dir / "cover_letter.pdf").exists()

        # Validate JSON contents
        with open(expected_dir / "job_application.json") as f:
            app_data = json.loads(f.read())
            assert app_data["job"]["id"] == "PYDEV-2025"
            assert app_data["application_form"][0]["question"] == "Experience"

    def test_file_content_integrity(self, tmp_path, job_application):
        """Verify copied files match original content"""
        with patch('job_application_saver.get_base_dir', return_value=str(tmp_path)):
            ApplicationSaver.save(job_application)
            
        target_dir = tmp_path / "PYDEV-2025 - Code Masters Inc Senior Python Developer"
        
        # Verify resume content
        original_resume = Path(job_application.job.resume_path).read_text()
        copied_resume = (target_dir / "resume.pdf").read_text()
        assert original_resume == copied_resume, "Resume content mismatch"
        
        # Verify cover letter content  
        original_cover = Path(job_application.job.cover_letter_path).read_text()
        copied_cover = (target_dir / "cover_letter.pdf").read_text()
        assert original_cover == copied_cover, "Cover letter content mismatch"

    def test_missing_files_handling(self, tmp_path, sample_job):
        """Verify behavior when resume/cover paths are empty"""
        sample_job.resume_path = ""
        sample_job.cover_letter_path = ""
        app = JobApplication(sample_job)
        
        with patch('job_application_saver.get_base_dir', return_value=str(tmp_path)):
            ApplicationSaver.save(app)
            
        target_dir = tmp_path / "PYDEV-2025 - Code Masters Inc Senior Python Developer"
        assert not (target_dir / "resume.pdf").exists()
        assert not (target_dir / "cover_letter.pdf").exists()

    def test_directory_naming_special_characters(self, tmp_path):
        """Verify handling of special characters in job metadata"""
        job = Job(
            id="DEV-123",
            title="Lead Developer (Python)",
            company="Tech & Code: Solutions",
            portal="Indeed",
            resume_path=str(tmp_path / "dummy.pdf"),
            cover_letter_path=str(tmp_path / "dummy.pdf")
        )
        
        # Create dummy files
        (tmp_path / "dummy.pdf").write_text("Dummy content")
        app = JobApplication(job)
        
        with patch('job_application_saver.get_base_dir', return_value=str(tmp_path)):
            ApplicationSaver.save(app)
            
        expected_dir = tmp_path / "DEV-123 - Tech & Code: Solutions Lead Developer (Python)"
        assert expected_dir.exists(), "Directory with special chars not created"

    def test_failed_save_directory(self, tmp_path, job_application):
        """Verify failed applications get special parent directory"""
        with patch('job_application_saver.get_base_dir', return_value=str(tmp_path)):
            ApplicationSaver.save(job_application, is_failed=True)
        
        # Calculate expected directory structure
        original_base = Path(tmp_path)
        failed_base = original_base.parent / f"failed_{original_base.name}"
        expected_dir = failed_base / "PYDEV-2025 - Code Masters Inc Senior Python Developer"
        
        assert expected_dir.exists(), "Failed directory structure incorrect"
        assert (expected_dir / "job_application.json").exists()

    def test_save_error_handling(self, tmp_path, job_application):
        """Verify error handling during file operations"""
        with patch('shutil.copy') as mock_copy:
            mock_copy.side_effect = Exception("File copy failed")
            with patch('job_application_saver.get_base_dir', return_value=str(tmp_path)):
                with pytest.raises(Exception) as exc_info:
                    ApplicationSaver.save(job_application)
                
        assert "File copy failed" in str(exc_info.value)
