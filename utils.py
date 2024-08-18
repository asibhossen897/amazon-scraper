import re
import os
import csv
import requests


def format_title(title):
    # Remove any characters that are not alphanumeric or spaces
    title = re.sub(r'[^a-zA-Z0-9 ]', '', title)

    # Replace spaces with underscores
    title = title.replace(' ', '_')
    return title


def save_img(path, title, link):
    with open(f"{path}/{title}.jpg", 'wb') as f:
        f.write(requests.get(link).content)
        print("Image saved successfully.")


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def write2csv(filename, fields, mode='w', newline='', encoding='utf-8'):
    """
    Writes data to a CSV file.

    :param filename: The name of the CSV file to write to.
    :param fields: A list of dictionaries where keys are the CSV headers.
    :param mode: File mode, 'w' for write (default) or 'a' for append.
    :param newline: Controls how universal newlines mode works (default is '').
    :param encoding: The file encoding (default is 'utf-8').
    """
    if not fields:
        print("No data to write.")
        return

    # Extract fieldnames from the first dictionary's keys
    fieldnames = fields[0].keys()

    try:
        with open(filename, mode, newline=newline, encoding=encoding) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if mode == 'w':  # Write header only in write mode
                writer.writeheader()

            writer.writerows(fields)

        print(f"Data successfully written to {filename}")

    except IOError as e:
        print(f"Error writing to file {filename}: {e}")
