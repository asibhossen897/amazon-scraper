import requests
from seleniumbase import Driver
driver = Driver()


def scrape():
    filename = r'links.txt'
    with open(filename, 'r') as f:
        links = f.readlines()

    for link in links:
        driver.open(link)
        driver.wait_for_element("main h1")
        soup = driver.get_beautiful_soup()
        title = soup.select("h1")
        print(title)


scrape()