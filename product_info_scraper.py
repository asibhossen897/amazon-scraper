from seleniumbase import BaseCase
from utils import write2csv
from bs4 import BeautifulSoup

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

                # Find the element containing the rating for each product
                product_container = link.find_parent("div", class_="sg-col-inner")

                rating_text = None
                total_review = None

                if product_container:
                    rating_element = product_container.find("span", class_="a-icon-alt")
                    if rating_element:
                        rating_text = rating_element.get_text(strip=True)
                        rating_text = rating_text.split(' ')[0]

                    total_review = product_container.find("div", {"data-csa-c-slot-id": "alf-reviews"})
                    if total_review:
                        total_review = total_review.get_text(strip=True)

                # Refine the price extraction
                original_price = None
                discounted_price = None
                price_container = product_container.find("div", {"data-cy": "price-recipe"})

                if price_container:
                    # Extract original price
                    original_price_span = price_container.find("span", class_="a-price a-text-price")
                    if original_price_span:
                        original_price = original_price_span.find("span", class_="a-offscreen")
                        if original_price:
                            original_price = original_price.get_text(strip=True)

                    # Extract discounted price
                    discounted_price_span = price_container.find("span", class_="a-price")
                    if discounted_price_span:
                        discounted_price = discounted_price_span.find("span", class_="a-offscreen")
                        if discounted_price:
                            discounted_price = discounted_price.get_text(strip=True)

                # Combine the link, title, and rating in a dictionary
                data.append({"link": full_url, "title": title, "rating_text": rating_text, "total_review": total_review, "original_price": original_price, "discounted_price": discounted_price})

        filename = f"src/{search_query.replace('+', '_')}_links.csv"
        write2csv(filename, data)
