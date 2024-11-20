import requests
from bs4 import BeautifulSoup
import time

base_url_1 = "https://www.lrytas.lt/"

def crawling(url, timeout):
    start_time = time.time() #starting the timer
    title_list = [] #create empty list to store titles in

    try:
        response = requests.get(url) #send get request to URL
        response.raise_for_status() #check for HTTP errors

        soup = BeautifulSoup(response.content, "html.parser")
        #parse - break down the content with beautifulsoup

        article_titles = soup.find_all('h2', class_='text-base font-medium text-black-custom')
        #find all articles by title name and class

        for title in article_titles:
            if time.time() - start_time > timeout: #check elapsed time
                print("Timeout reached - stopping the function")
                break #if time is exceeded, stop loop

            link = title.find('a')
            title_list.append(link.text.strip()) #add titles to title list

    except requests.exceptions.RequestException as error:
        #cathces errors during HTTP request
        print(f"Request failed: {error}")

    except Exception as error:
        #catches unexpected errors
        print(f"An error occurred: {error}")

    finally:
        #runs after the function is finished
        print("Crawling attempt finished")

    return title_list #return the title list

titles = crawling("https://www.lrytas.lt/", 5)

for index, title in enumerate(titles, start=1):
    print(f"{index}. {title}")