import requests
from bs4 import BeautifulSoup
import time

def crawling(url, timeout):

    """
    Crawl articles from specified URL and return the article titles and associated image URLs.
    :param url: https://www.lrytas.lt/
    :param timeout: set maximum time in seconds to run the crawl before stopping
    :return: List of tuples (article_title, image_url)
    """
    start_time = time.time()
    #starting the timer
    articles = []
    #create empty list to store articles in

    try:
        response = requests.get(url)
        #send get request to URL
        response.raise_for_status()
        #check for HTTP errors

        soup = BeautifulSoup(response.content, "html.parser")
        #parse - break down the content with beautifulsoup

        article_titles = soup.find_all('h2', class_='text-base font-medium text-black-custom')
        #find all articles by title name and class

        for title in article_titles:
            if time.time() - start_time > timeout:
                #check elapsed time
                print("Timeout reached - stopping the function")
                break
                #if time is exceeded, stop loop

            link = title.find('a')
            article_title = link.text.strip()
            #add titles to title list

            image_tag = title.find_previous('img')
            #search for the closest image element
            image_url = image_tag['src'] if image_tag else None
            #get the 'src' attribute of the image_tag

            articles.append((article_title, image_url))
            # add titles and image urls to list


    except requests.exceptions.RequestException as error:
        #cathces errors during HTTP request
        print(f"Request failed: {error}")

    except Exception as error:
        #catches unexpected errors
        print(f"An error occurred: {error}")

    finally:
        #runs after the function is finished
        print("Crawling attempt finished")

    return articles #return the title list