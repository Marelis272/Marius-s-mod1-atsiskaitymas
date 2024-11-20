import requests
from bs4 import BeautifulSoup
import time
import csv

def crawling(url, timeout, format='list'):

    """
    Crawl articles from specified URL and return the article titles and associated image URLs.
    :param url:
        The URL of the website to crawl e.g. "https://www.lrytas.lt/"
    :param timeout:
        The maximum time in seconds to run the crawl before stopping
    :param format:
        The format in which to return the data ('list' or 'csv')
    :return:
        List of tuples, where each tuple contains the article title and attached image URL
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

    if format == 'list':
        #if format is list, return as is
        return articles
    elif format == 'csv':
        #if format is csv return csv file
        with open('articles.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Image URL'])
            for article in articles:
                writer.writerow(article)
        return "CSV file created successfully"
    else:
        #else return error - unsupported format
        raise ValueError("Unsupported output format, please choose 'list' or 'csv'")