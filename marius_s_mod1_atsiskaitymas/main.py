import sys
from crawler import crawling

def main():
    if len(sys.argv) != 4:
        #check if there are 4 arguments
        print("Usage: python main.py <site> <timeout> <format>")
        #usage instructions for the function
        sys.exit(1)

    site = sys.argv[1]
    #Choose site to crawl with crawling function
    timeout = int(sys.argv[2])
    #Set the timeout in seconds
    format = sys.argv[3]
    #Set the format option for output ('list' or 'csv')

    articles = crawling(site, timeout, format)

    if format == 'list':
        for index, (title, image_url) in enumerate(articles, start=1):
            print(f"{index}. {title}\nImage: {image_url}")
    elif format == 'csv':
        print(articles)
    else:
        print("Unknown format selected")

if __name__ == "__main__":
    main()