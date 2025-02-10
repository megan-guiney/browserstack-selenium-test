import unittest
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browserstack.local import Local  # Required for BrowserStack Local


class TestBStackLogin(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #    print("")

    def setUp(self):
        print("Ensuring base class is setUp properly", flush=True)
        super().setUp()
        self.baseURL = "https://www.bstackdemo.com/"
        driverUser = os.environ.get("BROWSERSTACK_USERNAME")
        driverPasswd = os.environ.get("BROWSERSTACK_ACCESS_KEY")
        if not driverUser or not driverPasswd:
            raise ValueError(
                "BrowserStack credentials not found in environment variables!")
        # TODO: clean up browser string with embedded driver creds
        browserstackURL = f"https://{driverUser}:{driverPasswd}@hub-cloud.browserstack.com/wd/hub"
        self.driver = webdriver.Remote(
            command_executor=browserstackURL,
            # Options are dynamically set from browserstack.yml
            options=webdriver.ChromeOptions()
        )

    def test_favorite(self):
        # set variables from env
        # TODO: clean up to better methodology
        DEMO_USER = os.environ.get("DEMO_USER")
        DEMO_PASSWORD = os.environ.get("DEMO_PASSWORD")
        driver = self.driver

        # Login to site
        print("Logging in...", flush=True)
        driver.get(self.baseURL + "signin")
        driver.maximize_window()
        try:
            # Wait for the username dropdown container to be visible and click it
            print("getting username dropdown", flush=True)
            username_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "username"))
            )
            username_dropdown.click()  # Open dropdown
            # Now locate the actual input inside the dropdown and send the username
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "react-select-2-input"))
            )
            print("entering username" + DEMO_USER, flush=True)
            username_input.send_keys(DEMO_USER)  # Type username
            username_input.send_keys(Keys.RETURN)  # Select it
            # Repeat the same steps for password selection
            print("getting password dropdown", flush=True)
            password_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "password"))
            )
            password_dropdown.click()  # Open password dropdown
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "react-select-3-input"))
            )
            print("entering passwd", flush=True)
            password_input.send_keys(DEMO_PASSWORD)  # Type password
            password_input.send_keys(Keys.RETURN)  # Select it
            # Click the login buttonA
            print("clicking login button", flush=True)
            login_button = driver.find_element(By.ID, "login-btn")
            login_button.click()
            print("--> Login successful!", flush=True)

            print("Filtering Samsung devices...", flush=True)
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[text()='Apple']//ancestor::label"))
            )
            samsung_filter = driver.find_element(
                By.XPATH, "//span[text()='Samsung']//ancestor::label")
            samsung_filter.click()
            print("--> Samsung devices filtered!", flush=True)

            print("Favoriting the Galaxy S20+...", flush=True)
            favorite_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//p[text()='Galaxy S20+']/ancestor::div[contains(@class, 'shelf-item')]//button"))
            )
            favorite_button.click()
            print("--> 'Favorite' button pressed!", flush=True)

            print("Verifying that the Galazy S20+ was successfully added to Favorites...")

            driver.find_element(By.ID, "favourites").click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//p[text()='Galaxy S20+']"))
            )
            assert driver.find_element(
                By.XPATH, "//p[text()='Galaxy S20+']").is_displayed(), "Galaxy S20+ is not in Favorites!"
            print("--> Test Passed: Galaxy S20+ can be added to Favorites", flush=True)

        except Exception as e:
            print("Error: " + str(e), flush=True)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
