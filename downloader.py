from utils import *
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ScrapeAmazon(BaseCase):
    def test_scrape(self):
        filename = r'links.txt'
        with open(filename, 'r') as f:
            links = f.readlines()

        for link in links:
            self.open(link)
            self.wait_for_element("h1")
            soup = self.get_beautiful_soup()
            title = soup.find(id="title")
            title = title.get_text().strip()
            product_img = soup.find(id="landingImage")
            if product_img:
                product_img_url = product_img.get("src")
                # Split the URL at the last dot before the file extension
                base_url = product_img_url.split('._')[0]  # Split on '._' to remove the transformation part
                final_url = base_url + ".jpg"  # Reconstruct the URL without the transformation part

                path = "images"
                mkdir(path)
                save_img(path, title, final_url)
            else:
                print("Product image not found.")

