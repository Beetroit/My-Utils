import gc
import os
import requests
import time
from selenium.webdriver import ChromeOptions
import random
import logging

logger = logging.getLogger("selenium")
logger.setLevel(logging.INFO)

android_ua = "Mozilla/5.0 (Linux; Android 14; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36"



def get_options(headless=False, platform ='win32'):
    """
    Get Chrome options based on the provided parameters.

    Args:
        headless (bool): Whether to run Chrome in headless mode. Default is False.
        platform (str): The platform to run Chrome on. Default is 'win32'.

    Returns:
        ChromeOptions: The configured Chrome options.
    """
    options = ChromeOptions()

    if platform == 'android':
        # Configure Chrome to run on Android device
        mobile_emulation = {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "
                         "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
            "clientHints": {"platform": "Android", "mobile": True}
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)

    if headless:
        # Configure Chrome to run in headless mode
        options.add_argument("--headless")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--window-size=1080,1920")
    options.add_argument("excludeSwitches=enable-automation")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1,
        },
    )

    chrome_home = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data")
    print(chrome_home)

    options.add_argument(f"--user-data-dir={chrome_home}")

    return options


def nav_update():
    """
    Scroll the window until the page is fully loaded.

    This function uses JavaScript to scroll the window and checks the current
    position after each scroll. It continues scrolling until the current
    position is the same as the previous position or until it reaches a maximum
    number of scrolls.

    Feel free to modify the break condition, mine uses checks for the bottom of the page, you can use a time diff or number of scrolls or a combination

    usage:  driver.get(url)
            nav_update() #scrolls the page

    :return: None
    """

    try:
        pass
    except Exception as e:
        pass

    # Get the current vertical position of the window
    x = driver.execute_script("return window.pageYOffset")

    new = 1
    count = 0

    while x != new:
        gc.collect()

        try:
            # Scroll the window by 1000 pixels
            driver.execute_script("return window.scrollBy(0,1000)")
            time.sleep(2)
            new = x
            x = driver.execute_script("return window.pageYOffset")
        except:
            pass

        x = driver.execute_script("return window.pageYOffset")

        if x == new: # if count == n
            break

        count += 1
def get_proxies():
    """
    Get a list of proxies from an API and save them to a file.
    
    Returns:
        proxies (list): A list of proxy URLs.
    """
    anonymity = "elite" # "anonymous", "transparent", "all"
    country = "US" # "CA", "AU", "BR", "IN", "JP", "MX", "RU", "TW", "UK", "US", "all"
    ssl = "yes" # "yes", "no"
    protocol = "http" # "http", "https", "Socks4", "Socks5"
    # Define the API URL
    proxy_url = f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout=10000&country={country}&ssl={ssl}&anonymity={anonymity}"
    
    # Make a request to the API
    r = requests.get(proxy_url)
    
    # Split the response into a list of proxies
    proxies = [i.strip() for i in r.text.splitlines()]
    
    # Save the proxies to a file
    with open("proxies.txt", "w") as f:
        for proxy in proxies:
            f.write(f"{proxy}\n")
    
    # Shuffle the list of proxies
    random.shuffle(proxies)
    
    # Print the first proxy in the shuffled list
    print(proxies[0])
    
    # Return the list of proxies
    return proxies
