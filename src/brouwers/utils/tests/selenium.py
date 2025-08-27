import os
from unittest import skipIf

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings, tag
from django.utils.module_loading import import_string

SELENIUM_WEBDRIVER = os.getenv("SELENIUM_WEBDRIVER", default="Chrome")
SELENIUM_HEADLESS = "NO_SELENIUM_HEADLESS" not in os.environ

if SELENIUM_WEBDRIVER:
    WebDriver = import_string(f"selenium.webdriver.{SELENIUM_WEBDRIVER}")
    Options = import_string(
        f"selenium.webdriver.{SELENIUM_WEBDRIVER.lower()}.options.Options"
    )
else:
    WebDriver, Options = None, None


skipUnlessSelenium = skipIf(not WebDriver, "No Selenium webdriver configured")


@tag("e2e")
@override_settings(ALLOWED_HOSTS=["*"])
class SeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        assert WebDriver, (
            "Selenium must be configured, see the SELENIUM_WEBDRIVER envvar"
        )
        assert Options, "Selenium must be configured, see the SELENIUM_WEBDRIVER envvar"

        options = Options()
        if SELENIUM_HEADLESS:
            options.headless = True
            options.add_argument("--headless=new")  # for Chrome >= 109

        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
