import time
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# STOCK SYMBOLS [$SPX, $TSLA, $SOFI, $APPL]

chrome_options = webdriver.ChromeOptions()

first_session = True

# Inputs
# twitter_accounts = [str(account) for account in input("Input Twitter Accounts \n").split()]
twitter_accounts = ['https://twitter.com/Mr_Derivatives', 'https://twitter.com/warrior_0719',
                    'https://twitter.com/ChartingProdigy', 'https://twitter.com/allstarcharts',
                    'https://twitter.com/yuriymatso', 'https://twitter.com/TriggerTrades',
                    'https://twitter.com/AdamMancini4', 'https://twitter.com/CordovaTrades',
                    'https://twitter.com/Barchart', 'https://twitter.com/RoyLMattox']
stock_symbol = str(input("Stock Symbol \n"))
time_interval = int(input("Time Interval In Minutes \n"))


def scrape_twitter_accounts(twitter_accounts: list, stock_symbol: str) -> str:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    no_of_occurrences = 0
    for twitter_account in twitter_accounts:
        driver.get(twitter_account)
        # to make find elements by xpath case-insensitive
        xpath = "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '%s')]" % stock_symbol.lower()
        try:
            elements = WebDriverWait(driver, timeout=5).until(ec.presence_of_all_elements_located((By.XPATH, xpath)))
            if elements:
                no_of_occurrences += len(elements)
        except TimeoutException:
            continue
    driver.quit()
    if no_of_occurrences > 0:
        msg = "%s was mentioned %s times" % (stock_symbol, no_of_occurrences)
    else:
        msg = "%s was not found" % stock_symbol
    if not first_session:
        msg += " in the last %s minutes" % str(time_interval)
    return msg


while True:
    print(scrape_twitter_accounts(twitter_accounts=twitter_accounts, stock_symbol=stock_symbol))
    if first_session:
        first_session = False
    time.sleep(time_interval * 60)
