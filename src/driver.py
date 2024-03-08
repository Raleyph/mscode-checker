import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

from fake_useragent import UserAgent
from filemanager import FileManager


class MSDriver:
    def __init__(self, filemanager: FileManager) -> None:
        self.__TARGET_LINK = "https://account.microsoft.com/billing/redeem?refd=account.microsoft.com"
        self.__INPUT_ID = "tokenString"
        self.__CODE_ERROR_CLASSNAME = "redeem_code_error"

        self.__filemanager = filemanager

        self.__driver = webdriver.Chrome(
            options=self.__get_driver_options(),
            service=Service(executable_path="chromedriver.exe")
        )

        self.__driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """
        })

        self.__driver.get(self.__TARGET_LINK)
        self.__driver_wait = WebDriverWait(self.__driver, 60)

    def __del__(self):
        self.__driver.close()

    @staticmethod
    def __get_driver_options():
        useragent = UserAgent()
        options = Options()

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument(f"--user-agent={useragent.random}")

        options.add_experimental_option("detach", True)

        return options

    def __is_logged(self) -> bool:
        while self.__driver.current_url != self.__TARGET_LINK:
            continue

        frame = self.__driver_wait.until(ec.presence_of_element_located((By.TAG_NAME, "iframe")))

        if not frame:
            return False

        self.__driver.switch_to.frame(frame)

        try:
            self.__driver_wait.until(ec.presence_of_element_located((By.ID, self.__INPUT_ID)))
        except TimeoutException:
            return False

        return True

    def __is_code_valid(self, code_input: WebElement, code: str) -> bool:
        code_input.clear()
        code_input.send_keys(code)

        try:
            WebDriverWait(self.__driver, 3).until(
                ec.presence_of_element_located((By.CLASS_NAME, self.__CODE_ERROR_CLASSNAME))
            )
        except TimeoutException:
            return True

        return False

    def start(self) -> bool:
        if not self.__is_logged():
            return False

        code_input = self.__driver.find_element(By.ID, self.__INPUT_ID)

        for code in self.__filemanager.get_codes():
            if self.__is_code_valid(code_input, code):
                self.__filemanager.write_valid_code(code)
            time.sleep(3)

        return True
