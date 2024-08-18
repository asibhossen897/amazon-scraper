from seleniumbase import BaseCase
from utils import write2csv, save_img
from bs4 import BeautifulSoup

BaseCase.main(__name__, __file__)


class ProductLinkScraper(BaseCase):

    def test_scrape_product_info(self):
        search_query = "Math books"
        start_page = 1  # Starting page
        end_page = 3  # Last page to scrape

        data = []
        for page_number in range(start_page, end_page + 1):
            url = self.build_search_url(search_query, page_number)
            self.open(url)
            self.wait_for_element("h2")  # Wait for the page to load

            soup = BeautifulSoup(self.get_page_source(), 'html.parser')
            data.extend(self.extract_product_data(soup))

            if not self.has_next_page(soup, current_page=page_number, end_page=end_page):
                break

        self.save_to_csv(search_query, start_page, end_page, data)

    def build_search_url(self, search_query, page_number):
        formatted_query = search_query.replace(" ", "+").lower()
        return f"https://www.amazon.com/s?k={formatted_query}&page={page_number}"

    def extract_product_data(self, soup):
        product_data = []
        product_links = soup.find_all("a",
                                      class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")

        for link in product_links:
            href = link.get("href")
            if "dp" in href and "sspa" not in href:  # Ensure it's a product link
                product_data.append(self.extract_product_details(link))

        return product_data

    def extract_product_details(self, link):
        dp = link.get("href").split("/")[-2]
        full_url = f"https://www.amazon.com/dp/{dp}"
        title = link.get_text(strip=True)
        product_container = link.find_parent("div", class_="sg-col-inner")

        rating_text, total_review = self.extract_rating_and_reviews(product_container)
        original_price, discounted_price = self.extract_prices(product_container)
        product_img_url = self.get_img_link(product_container)
        return {
            "link": full_url,
            "title": title,
            "rating_text": rating_text,
            "total_review": total_review,
            "original_price": original_price,
            "discounted_price": discounted_price,
            "product_img_url": product_img_url
        }

    def extract_rating_and_reviews(self, container):
        rating_text = None
        total_review = None

        if container:
            rating_element = container.find("span", class_="a-icon-alt")
            if rating_element:
                rating_text = rating_element.get_text(strip=True).split(' ')[0]

            total_review_element = container.find("div", {"data-csa-c-slot-id": "alf-reviews"})
            if total_review_element:
                total_review = total_review_element.get_text(strip=True)

        return rating_text, total_review

    def extract_prices(self, container):
        original_price = None
        discounted_price = None
        price_container = container.find("div", {"data-cy": "price-recipe"})

        if price_container:
            original_price = self.get_price_from_span(price_container, "span", "a-price a-text-price")
            discounted_price = self.get_price_from_span(price_container, "span", "a-price")

        return original_price, discounted_price

    def get_price_from_span(self, container, tag_name, class_name):
        span_element = container.find(tag_name, class_=class_name)
        if span_element:
            price = span_element.find("span", class_="a-offscreen")
            if price:
                return price.get_text(strip=True)
        return None

    def get_img_link(self, container):
        img_element = container.find("img", {"data-image-latency": "s-product-image"})
        if img_element:
            img_url = img_element.get("data")

            # Split the URL at the last dot before the file extension
            base_url = img_url.split('._')[0]  # Split on '._' to remove the transformation part
            final_url = base_url + ".jpg"  # Reconstruct the URL without the transformation part
            return final_url
        return None

    def has_next_page(self, soup, current_page, end_page):
        next_button = soup.find("a",
                                class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")
        return next_button and "s-pagination-disabled" not in next_button.get("class", []) and current_page < end_page

    def save_to_csv(self, search_query, start_page, end_page, data):
        filename = f"data/{search_query.replace('+', '_')}_links_page_{start_page}_to_{end_page}.csv"
        write2csv(filename, data)
