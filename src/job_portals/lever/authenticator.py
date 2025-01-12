from src.ai_hawk.authenticator import AIHawkAuthenticator

class LeverAuthenticator(AIHawkAuthenticator):

    @property
    def home_url(self):
        raise NotImplementedError

    def navigate_to_login(self):
        raise NotImplementedError

    def handle_security_checks(self):
        raise NotImplementedError

    @property
    def is_logged_in(self):
        raise NotImplementedError

    def __init__(self, driver):
        super().__init__(driver)
    
    def start(self):
        pass
