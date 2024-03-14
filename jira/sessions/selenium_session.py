import json
import urllib
from time import sleep
from urllib.parse import urlencode
from webbrowser import Chrome

from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.common.by import By


class SeleniumSession:
    def __init__(self, options, driver: ChromiumDriver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.options = options

    def get(self, url, params=None, headers=None):
        if params:
            params = urlencode(params)
            url = f"{url}?{params}"
        self.driver.get(url)
        html = self.driver.find_element(by=By.TAG_NAME, value="body").text
        return html

    def post(self, url, params=None, data=None, headers=None):
        data: dict = data or {}
        javascript = f"""
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "{url}", true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onload = function () {{
            if (this.status >= 200 && this.status < 400) {{
        document.body.innerHTML = this.responseText;
        console.log(this.responseText);
    }} else {{
        // Handle any errors that occur during the request
        console.error('Request failed: ' + this.status);
    }}
        }};
        xhr.send({json.dumps(data)});
        """
        self.driver.execute_script(javascript)
        sleep(2)
        html = self.driver.find_element(by=By.TAG_NAME, value="body").text
        return html
