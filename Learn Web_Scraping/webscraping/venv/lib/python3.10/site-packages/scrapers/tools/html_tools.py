from lxml import html
import requests
from urllib.parse import (
        urljoin, urlencode, unquote, urlparse, parse_qsl, ParseResult
    )
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .generic_tools import singleton, clean_xpath_res


def current_page(url, page_argument):
    parsed_get_args = dict(parse_qsl(urlparse(unquote(url)).query))
    return int(parsed_get_args.get(page_argument, 1))

def next_url_page_argument(url, page_argument):
    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))
    parsed_get_args[page_argument] = int(parsed_get_args.get(page_argument, 1)) + 1
    # Converting URL argument to proper query string
    encoded_get_args = urlencode(parsed_get_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()
    return new_url

def next_url_xpath(url, page_html, next_page_xpath):
    return urljoin(url, clean_xpath_res(page_html.xpath(next_page_xpath)))


def next_url(url, page_argument=None, page_html=None, next_page_xpath=None):
    if page_argument is None:
        next_link = next_url_xpath(url, page_html, next_page_xpath)
    else:
        next_link = next_url_page_argument(url, page_argument)
    return next_link


@singleton
def get_driver(headless=True):
    chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
    if headless:
        chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_html(url, use_chrome=False, headless=True, force_new=False):
    if use_chrome:
        driver = get_driver(force_new=force_new, headless=headless)
        driver.get(url)
        page_content = driver.page_source
    else:
        page_content = requests.get(url).content

    page_html = html.fromstring(page_content)

    return page_html

