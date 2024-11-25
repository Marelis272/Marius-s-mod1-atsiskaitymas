import requests
from lxml import html
from urllib.parse import urljoin
import time
import csv

def crawling(site='https://www.lrytas.lt/', timeout=10, format='list'):

    """
    Crawl articles from specified URL and return the article titles and associated image URLs.
    :param site:
        The site to crawl ('https://www.lrytas.lt/' or 'https://kauno.diena.lt/')
    :param timeout:
        The maximum time in seconds to run the crawl before stopping
    :param format:
        The format in which to return the data ('list' or 'csv')
    :return:
        List of tuples, where each tuple contains the article title and attached image URL
    """
    start_time = time.time() #start the timer
    articles = []

    #site specific paths
    if site == 'https://www.lrytas.lt/':
        url = 'https://www.lrytas.lt/'
        title_path = "//h2[contains(@class, 'text-base') and contains(@class, 'font-medium') and contains(@class, 'text-black-custom')]/a[1]/text()"
        image_path = "//div[contains(@class, 'rounded-[4px]')]/a/img/@src"

    elif site == 'https://kauno.diena.lt/':
        url = 'https://kauno.diena.lt/'
        title_path = "//a[contains(@class, 'articles-list-title')]/text()"
        image_path = ".//div[contains(@class, 'articles-list-media')]//img"

    else:
        raise ValueError("Unsupported site, please choose 'https://www.lrytas.lt/' or 'https://kauno.diena.lt/'")

    try:
        response = requests.get(url)
        response.raise_for_status()
        tree = html.fromstring(response.content)

        titles = tree.xpath(title_path)
        images = tree.xpath(image_path)

        #loop through titles and images while keeping track of time
        for title, img in zip(titles, images):
            if time.time() - start_time > timeout:
                print("Timeout reached - function stopped")
                break

            if isinstance(title, str):
                article_title = title.strip()
            elif hasattr(title, 'text'):
                article_title = title.text.strip() if title.text else None
            else:
                article_title = None

            if not article_title:
                print("Skipping article with no title")
                continue

            if isinstance(img, str):
                image_url = img
            elif hasattr(img, 'get'):
                image_url = img.get("data-src") or img.get("src")
            else:
                image_url = None

            if image_url and "blank.gif" not in image_url:
                image_url = urljoin(url, image_url)
            else:
                print(f"Skipping article {article_title} with an invalid or missing image URL")
                continue

            articles.append((article_title, image_url))

    except requests.exceptions.RequestException as error:
        #cathces errors during HTTP request
        print(f"Request failed: {error}")

    except ValueError as value_error:
        print(f"Error: {value_error}")

    except Exception as error:
        #catches unexpected errors
        print(f"An error occurred: {error}")

    finally:
        #runs after the function is finished
        print("Crawling attempt finished")

    if format == 'list':
        return articles
    elif format == 'csv':
        csv_file = "articles.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Image URL"])
            writer.writerows(articles)
        print(f"CSV file '{csv_file}' created successfully.")
        return csv_file
    else:
        raise ValueError("Unsupported format, please choose 'list' or 'csv'")