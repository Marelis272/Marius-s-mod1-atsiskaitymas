import sys
from crawler import crawling

def main():
    if len(sys.argv) != 3:
        #check if there are 3 arguments
        print("Usage: python main.py <URL> <timeout>")
        #usage instructions for the function
        sys.exit(1)

    url = sys.argv[1]
    #Choose URL to crawl with crawling function
    timeout = int(sys.argv[2])
    # Set the timeout in seconds

    articles = crawling(url, timeout)