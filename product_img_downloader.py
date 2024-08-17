import pandas as pd
from utils import *
import concurrent.futures
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ScrapeAmazon(BaseCase):
    def test_scrape(self):
        filename = r'src/python_book_links.csv'

        # Read the CSV file and get links from the 'link' column
        links_df = pd.read_csv(filename)
        links = links_df['link'].tolist()

        for link in links:
            self.open(link)
            self.wait_for_element("h1")
            soup = self.get_beautiful_soup()

            # Extract the product title
            title = soup.find(id="title")
            title = title.get_text().strip()

            # Extract the product image link
            product_img = soup.find(id="landingImage")
            if product_img:
                product_img_url = product_img.get("src")
                # Split the URL at the last dot before the file extension
                base_url = product_img_url.split('._')[0]  # Split on '._' to remove the transformation part
                final_url = base_url + ".jpg"  # Reconstruct the URL without the transformation part

                # Saving the image to a certain directory
                path = "images"
                mkdir(path)
                save_img(path, title, final_url)
            else:
                print("Product image not found.")
