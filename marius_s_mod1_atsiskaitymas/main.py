import requests
from bs4 import BeautifulSoup
import time

base_url_1 = "https://www.lrytas.lt/"

def crawling(url, timeout):
    start_time = time.time()
    title_list = []

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        article_titles = soup.find_all('h2', class_='text-base font-medium text-black-custom')

        for title in article_titles:
            if time.time() - start_time > timeout:
                print("Timeout reached - stopping the function")
                return
            link = title.find('a')
            title_list.append(link.text.strip)

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")

    except Exception as error:
        print(f"An error occurred: {error}")

    finally:
        print("Crawling attempt finished")