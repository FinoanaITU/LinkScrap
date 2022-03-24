from selenium import webdriver
from pprint import pprint
import os
# from webdriver_manager.chrome import ChromeDriverManager

class chrome ():

    def __init__(self,basedir):
        self.basedir = basedir

    def driver(self):
        print('ouverture chromedriver')
        chrome_options = webdriver.ChromeOptions()

        # driver_location  = "/usr/local/bin/chromedriver"
        # driver_location  = "/usr/lib/chromium-browser/chromedriver"
        # binary_location  = " /usr/bin/google-chrome"
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--ignore-ssl-errors')
        # chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--no-sandbox")
        # driver = webdriver.Chrome(executable_path="C:\\Program Files\\Chromedriver\\Chromedriver.exe",chrome_options=chrome_options)
        prefs = {
            "download.default_directory" : "D:\\Perso",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
            }
        chrome_options.add_experimental_option("prefs",prefs)
        chrome_options.page_load_strategy = 'normal'
        # chrome_options.binary_location = binary_location

        #for windows
        driver = webdriver.Chrome(executable_path="C:\\WebDriver\\bin\\chromedriver.exe",chrome_options=chrome_options)
        driver.maximize_window()
        #for linux
       # webdriver.Chrome(ChromeDriverManager().install())
        # driver =  webdriver.Chrome(executable_path=driver_location, chrome_options=chrome_options)

        # driver = webdriver.Chrome(ChromeDriverManager().install())
        # driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        # params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': "D:\\Perso"}}
        # command_result = driver.execute("send_command", params)
        # pprint(command_result)

        return driver
