import csv
from seleniumbase import BaseCase
from utils import *
BaseCase.main(__name__, __file__)


class ProductLinkScraper(BaseCase):
    def test_scrape_product_links(self):
        search_query = "Python Book"
        search_query = search_query.replace(" ", "+").lower()

        url = f"https://www.amazon.com/s?k={search_query}"
        self.open(url)
        self.wait_for_element("h2")

        soup = self.get_beautiful_soup()
        data = []

        # Collect product links
        for link in soup.find_all("a",
                                  class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"):
            href = link.get("href")
            if "dp" in href and "sspa" not in href:  # Ensure it's a product link
                dp = href.split("/")[-2]
                full_url = f"https://www.amazon.com/dp/{dp}"

                # Collect Product Title
                title = link.get_text(strip=True)

                # Combine the link and title in a dictionary
                data.append({"link": full_url, "title": title})

        write2csv(f"{search_query.replace('+', '_')}_links.csv", data)
