import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from utils import mkdir, save_img, format_title


def get_data_from_csv(filename):
    """Read the CSV file and return the list of links and formatted titles."""
    df = pd.read_csv(filename)

    # Extract lists of links and titles
    links = df['product_img_url'].tolist()
    titles = df['title'].tolist()

    # Format each title
    formatted_titles = [format_title(title) for title in titles]

    return links, formatted_titles


def download_image(link, title, path):
    """Download a single image and save it to the specified path."""
    try:
        save_img(path, title, link)
    except Exception as e:
        print(f"Error downloading {title}: {e}")


def download_images_concurrently(links, titles, path, max_workers=10):
    """Download images concurrently using threading."""
    mkdir(path)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(executor.map(lambda p: download_image(*p, path), zip(links, titles)), total=len(links)))


if __name__ == "__main__":
    filename = r'src/Headphones_links_page_1_to_3.csv'
    links, titles = get_data_from_csv(filename)
    path = "imgs"

    download_images_concurrently(links, titles, path, max_workers=10)
