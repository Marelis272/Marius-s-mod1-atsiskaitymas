import requests
from bs4 import BeautifulSoup
import time

base_url_1 = "https://www.lrytas.lt/"

def crawling(url, timeout):
    start_time = time.time() #starting the timer
    articles = [] #create empty list to store articles in

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
            article_title = link.text.strip() #add titles to title list

            image_tag = title.find_previous('img')
            #search for the closest image element
            image_url = image_tag['src'] if image_tag else None
            # get the 'src' attribute of the image_tag

            articles.append((article_title, image_url))


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


articles = crawling("https://www.lrytas.lt/", 5)

for index, (title, image_url) in enumerate(articles, start=1):
    #adds a number to each article in ascending order
    print(f"{index}. {title}")
    if image_url:
        print(f"Image: <a href='{image_url}'>Click here to view image</a>")
        #if there is an image print click here... instead of full image url
    else:
        print("Image: No image found")
        #else no image found