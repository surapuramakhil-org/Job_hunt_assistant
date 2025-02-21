<a name="top"></a>
<div align="center">
<img src="./assets/AIHawk.png">

# AIHawk the first Jobs Applier AI Agent

  [![Python Test Suite](https://github.com/surapuramakhil-org/Job_search_assistant/actions/workflows/py_test.yml/badge.svg?branch=main)](https://github.com/surapuramakhil-org/Job_search_assistant/actions/workflows/py_test.yml)

**🤖🔍 Your AI-powered job search assistant. Automate applications, get personalized recommendations, and land your dream job faster.**

[![Discord](https://img.shields.io/discord/1300208460788400159?style=for-the-badge&color=5865F2&logo=discord&logoColor=white&label=Discord)](https://discord.gg/MYYwG8JyrQ)

</div>

[Special thanks](#special-thanks) 

job search assistant is continuously evolving, and your feedback, suggestions, and contributions are highly valued. Feel free to open issues, suggest enhancements, or submit pull requests to help improve the project. Let's work together to make job search assistant a powerful tool for job seekers worldwide.

[Project Management Documentation](docs/project_management.md)
 

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Documentation](#documentation)
7. [Troubleshooting](#troubleshooting)
8. [Conclusion](#conclusion)
9. [Contributors](#contributors)
10. [License](#license)
11. [Disclaimer](#disclaimer)

## Introduction

job search assistant is a cutting-edge, automated tool designed to revolutionize the job search and application process. In today's fiercely competitive job market, where opportunities can vanish in the blink of an eye, this program offers job seekers a significant advantage. By leveraging the power of automation and artificial intelligence, job search assistant enables users to apply to a vast number of relevant positions efficiently and in a personalized manner, maximizing their chances of landing their dream job.

### The Challenge of Modern Job Hunting

In the digital age, the job search landscape has undergone a dramatic transformation. While online platforms have opened up a world of opportunities, they have also intensified competition. Job seekers often find themselves spending countless hours scrolling through listings, tailoring applications, and repetitively filling out forms. This process can be not only time-consuming but also emotionally draining, leading to job search fatigue and missed opportunities.

### Enter job search assistant: Your Personal Job Search Assistant

job search assistant steps in as a game-changing solution to these challenges. It's not just a tool; it's your tireless, 24/7 job search partner. By automating the most time-consuming aspects of the job search process, it allows you to focus on what truly matters - preparing for interviews and developing your professional skills.

## Features

1. **Intelligent Job Search Automation**
   - Customizable search criteria
   - Continuous scanning for new openings
   - Smart filtering to exclude irrelevant listings

2. **Rapid and Efficient Application Submission**
   - One-click applications
   - Form auto-fill using your profile information
   - Automatic document attachment (resume, cover letter)

3. **AI-Powered Personalization**
   - Dynamic response generation for employer-specific questions
   - Tone and style matching to fit company culture
   - Keyword optimization for improved application relevance

4. **Volume Management with Quality**
   - Bulk application capability
   - Quality control measures
   - Detailed application tracking

5. **Intelligent Filtering and Blacklisting**
   - Company blacklist to avoid unwanted employers
   - Title filtering to focus on relevant positions

6. **Dynamic Resume Generation**
   - Automatically creates tailored resumes for each application
   - Customizes resume content based on job requirements

7. **Secure Data Handling**
   - Manages sensitive information securely using YAML files

## Installation

**Confirmed successful runs on the following:**

- Operating Systems:
  - Windows 10
  - Ubuntu 22
  - macOS
- Python versions:
  - 3.13

## Prerequisites

Before you begin, ensure you have met the following requirements:

### Download and Install Python

Ensure you have the latest Python version installed (Python 3.11 or higher is required for this project). If not, download and install it from Python's official website. For detailed instructions, refer to the tutorials:
- [How to Install Python on Windows](https://docs.python.org/3/using/windows.html)
- [How to Install Python on Linux](https://docs.python.org/3/using/unix.html)
- [How to Download and Install Python on macOS](https://docs.python.org/3/using/mac.html)

### Download and Install Google Chrome

Download and install the latest version of Google Chrome in its default location from the [official website](https://www.google.com/chrome/).

### Install Poetry

Follow the instructions provided on Poetry's [official installation page](https://python-poetry.org/docs/#installation).

### Clone the Repository

```bash
git clone https://github.com/surapuramakhil-org/Job_hunt_assistant.git
cd Job_hunt_assistant
```

#### switching to stable versions

place to find release tags: https://github.com/surapuramakhil-org/Job_search_assistant/releases

```bash
git checkout <tag_name>
```

example:
```bash
git checkout v0.1.0-beta
```

### Setting Up the Project with Poetry

Since the project already includes a `pyproject.toml` file, follow these steps:

#### Install Dependencies

Run the following command in the project directory to install all dependencies specified in `pyproject.toml`:

```bash
poetry install
```

### Create `.env` File

To configure environment variables for the project, create a `.env` file by copying the `.env.template` file provided in the repository. This file will store sensitive information such as API keys and other configuration settings.

```bash
cp .env.template .env
```

After copying, open the `.env` file and fill in the required values. Ensure you do not share this file or commit it to version control, as it contains sensitive information.

### Usage 

0. **Account language**
   To ensure the bot works, your account language must be set to English.

1. **Data Folder:**
   Ensure that your data_folder contains the following files:
   - `secrets.yaml`
   - `config.yaml`
   - `plain_text_resume.yaml`

### For configuration refer [this docs](/docs/configuration.md)

2. **Output Folder:**
    Contains the output of the bot.
    - `data.json` results of the --collect mode
    - `failed.json` failed applications
    - `open_ai_calls.json` all the calls made to the LLM model
    - `skipped.json` applications that were skipped
    - `success.json` successful applications

    **Note:** `answers.json` is not part of the output folder and can be found in the root of the project. It is used to store the answers of the questions asked to the user. Can be used to update the bot with corrected answers. Search for `Select an option`, `0`, `Authorized`, and `how many years of` to verify correct answers.

3. **Run the Bot:**

   job search assistant offers flexibility in how it handles your pdf resume:

- **Dynamic Resume Generation:**
  If you don't use the `--resume` option, the bot will automatically generate a unique resume for each application. This feature uses the information from your `plain_text_resume.yaml` file and tailors it to each specific job application, potentially increasing your chances of success by customizing your resume for each position.

   ```bash
   poetry run python main.py
   ```

- **Using a Specific Resume:**
  If you want to use a specific PDF resume for all applications, place your resume PDF in the `data_folder` directory and run the bot with the `--resume` option:

  ```bash
  poetry run python main.py --resume /path/to/your/resume.pdf
  ```

- **Using the collect mode:**
  If you want to collect job data only to perform any type of data analytics you can use the bot with the `--collect` option. This will store in output/data.json file all data found,

  ```bash
  poetry run python main.py --collect
  ```
  
### For troubleshooting refer [this docs](/docs/troubleshooting.md)

### For Developers

- [Contribution Guidelines](docs/CONTRIBUTING.md)

- [Lang Chain Developer Documentation](https://python.langchain.com/v0.2/docs/integrations/components/)

- [Workflow diagrams](docs/workflow_diagrams.md)

## Supporting This Project

Supporting job search assistant helps us continue to develop and improve this valuable tool for job seekers worldwide. Here are a few ways you can contribute:

1. **Financial Contributions**: Consider making a donation. Your contributions help cover the costs of development, hosting, and other expenses. You can donate via [Giveth](https://giveth.io/project/job_hunt_assistant). Financial support enables faster development and more frequent releases.

2. **Spread the Word**: Share this project with your network. Whether it's through social media, blog posts, or word of mouth, spreading the word helps us reach more people who could benefit from job search assistant.

<div align="center">

[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/intent/tweet?text=Check%20out%20this%20awesome%20job%20search%20assistant%20tool%20powered%20by%20AI!%20Automate%20your%20job%20applications%20and%20land%20your%20dream%20job%20faster.%20%23JobSearchAssistant%20%23AI%20%23JobHunt%20%23Automation&url=https://github.com/surapuramakhil-org/Job_hunt_assistant)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/surapuramakhil-org/Job_hunt_assistant)
[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/sharer/sharer.php?u=https://github.com/surapuramakhil-org/Job_hunt_assistant)
[![Reddit](https://img.shields.io/badge/Reddit-FF4500?style=for-the-badge&logo=reddit&logoColor=white)](https://reddit.com/submit?url=https://github.com/surapuramakhil-org/Job_hunt_assistant&title=Check%20out%20this%20awesome%20job%20search%20assistant%20tool%20powered%20by%20AI!)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://api.whatsapp.com/send?text=Check%20out%20this%20awesome%20job%20search%20assistant%20tool%20powered%20by%20AI!%20Automate%20your%20job%20applications%20and%20land%20your%20dream%20job%20faster.%20%23JobSearchAssistant%20%23AI%20%23JobHunt%20%23Automation%20https://github.com/surapuramakhil-org/Job_hunt_assistant)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/share/url?url=https://github.com/surapuramakhil-org/Job_hunt_assistant&text=Check%20out%20this%20awesome%20job%20search%20assistant%20tool%20powered%20by%20AI!%20Automate%20your%20job%20applications%20and%20land%20your%20dream%20job%20faster.%20%23JobSearchAssistant%20%23AI%20%23JobHunt%20%23Automation)

[![Bluesky](https://img.shields.io/badge/Bluesky-0285FF?style=for-the-badge&logo=bluesky&logoColor=white)](https://bsky.app/intent/compose?text=Check%20out%20this%20awesome%20job%20search%20assistant%20tool%20powered%20by%20AI!%20Automate%20your%20job%20applications%20and%20land%20your%20dream%20job%20faster.%20%23JobSearchAssistant%20%23AI%20%23JobHunt%20%23Automation%20https://github.com/surapuramakhil-org/Job_hunt_assistant)


</div>

3. **Star the Repository**: If you find this project useful, please star the repository on GitHub. It helps increase the project's visibility and shows your appreciation.

4. **Join the Community**: Join our [Discord](https://discord.gg/MYYwG8JyrQ) to connect with other users and contributors. Your participation helps build a supportive community around the project.

5. **Report Issues / Feature requests**: If you encounter any bugs or have suggestions for improvements, please open an issue on [GitHub](https://github.com/surapuramakhil-org/Job_hunt_assistant/issues). Your feedback is crucial for the project's growth.

6. **Contribute Code**: If you're a developer, consider contributing code to the project. Check out our [Contribution Guidelines](docs/CONTRIBUTING.md), [PM docs](/docs/project_management.md)  for more information on how to get started.

Your support is greatly appreciated and helps us make job search assistant a powerful tool for job seekers everywhere.


## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=surapuramakhil-org/Job_hunt_assistant&type=Date)](https://star-history.com/#surapuramakhil-org/Job_hunt_assistant&Date)

If you like the project please star ⭐ the repository!

## Special Thanks
[![Contributors](https://img.shields.io/github/contributors/surapuramakhil-org/Job_hunt_assistant)](https://github.com/surapuramakhil-org/Job_hunt_assistant/graphs/contributors)

<a href="https://github.com/surapuramakhil-org/Job_hunt_assistant/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=surapuramakhil-org/Job_hunt_assistant" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## License

This project is licensed under the AGPL License. Documentation is licensed under CC BY - see the [AGPL LICENSE](LICENSE) and [CC BY LICENSE](docs/LICENSE) files for details.

The AGPL License requires that any derivative work must also be open source and distributed under the same license.

The CC BY License permits others to distribute, remix, adapt, and build upon your work, even for commercial purposes, as long as they credit you for the original creation. 
 

## Disclaimer

This tool, job search assistant, is intended for use at your own risk. The creators / maintainers / contributors assume no responsibility for any consequences arising from its use. Users are advised to comply with the terms of service of relevant platforms and adhere to all applicable laws, regulations, and ethical guidelines. The use of automated tools for job applications may carry risks, including potential impacts on user accounts. Proceed with caution and at your own discretion.

[Back to top 🚀](#top)
