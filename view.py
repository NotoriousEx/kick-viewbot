import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load proxies from file
def load_proxies(file_path):
    with open(file_path, 'r') as f:
        proxies = f.readlines()
    return [proxy.strip() for proxy in proxies]

# Initialize Chrome WebDriver with proxy
def init_driver(proxy):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=%s' % proxy)
    return webdriver.Chrome(options=chrome_options)

# Main function
def watch_kick_stream(kick_url, proxies_file):
    proxies = load_proxies(proxies_file)
    for proxy in proxies:
        try:
            driver = init_driver(proxy)
            driver.get(kick_url)
            stream_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='stream']")))
            stream_element.click()

            while True:
                if "Stream ended" in driver.page_source:
                    print("Stream ended. Exiting...")
                    break
                driver.refresh()
                time.sleep(30)  # Adjust delay as needed

        except Exception as e:
            print("An error occurred with proxy", proxy, ":", e)

        finally:
            if 'driver' in locals():
                driver.quit()

if __name__ == "__main__":
    kick_url = input("Enter the Kick page URL: ")
    proxies_file = "proxies.txt"  # Adjust filename as needed
    watch_kick_stream(kick_url, proxies_file)
