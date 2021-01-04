import sys
from selenium import webdriver

class Quiz:
    def __init__(self, url, combination_of_choices,
            chrome_path=r"driver\chromerdriver.exe"):
        if sys.platform != "win32":
            print("Sorry this operating system in not yet supported...")
            exit()
        self.url = url
        self.combination_of_choices = combination_of_choices
        self.chrome_path = chrome_path
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("useAutomationExtension",
                False)
        self.driver = webdriver.Chrome(executable_path=self.chrome_path,
                options=self.chrome_options)
        self.driver.get(self.url)
        time.sleep(1)
