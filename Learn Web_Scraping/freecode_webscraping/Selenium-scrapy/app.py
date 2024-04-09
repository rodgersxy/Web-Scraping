from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
from datetime import datetime

def get_currencies(currencies, start_date, end_date, export_csv=False):
    frames = []
    for currency in currencies:
        try:
            # Opening the connection and grabbing the page
            my_url = f'https://br.investing.com/currencies/usd-{currency.lower()}-historical-data'
            option = Options()
            option.headless = False  # Set to True for headless browsing
            driver = webdriver.Chrome(options=option)
            driver.get(my_url)
            driver.maximize_window()

            # Clicking on the date button
            date_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/section/div[8]/div[3]/div/div[2]/span")))
            date_button.click()

            # Sending the start and end dates (using datetime format)
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

            start_bar = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/input[1]")))
            start_bar.clear()
            start_bar.send_keys(start_date_obj.strftime('%d/%m/%Y'))

            end_bar = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/input[2]")))
            end_bar.clear()
            end_bar.send_keys(end_date_obj.strftime('%d/%m/%Y'))

            # Clicking on the apply button
            apply = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                            "/html/body/div[7]/div[5]/a")))
            apply.click()
            sleep(3)  # Adjust sleep time as needed

            # Getting the tables on the page and quiting
            dataframes = pd.read_html(driver.page_source)
            driver.quit()
            print(f'{currency} scraped.')

        except Exception as e:
            print(f'Failed to scrape {currency}: {e}')
            driver.quit()
            continue  # Move on to the next currency

        # Selecting the correct table
        for dataframe in dataframes:
            if dataframe.columns.tolist() == ['Date', 'Price', 'Open', 'High', 'Low', 'Change%']:
                df = dataframe
                break
        frames.append(df)

    # Exporting the .csv file (optional)
    if export_csv:
        df = pd.concat(frames, ignore_index=True)  # Combine all dataframes
        df.to_csv('data/currency.csv', index=False)
        print('currency.csv exported.')

# Example usage
currencies = ['eur', 'jpy', 'gbp']
start_date = '2023-01-01'
end_date = '2023-01-02'
get_currencies(currencies, start_date, end_date, export_csv=True)

