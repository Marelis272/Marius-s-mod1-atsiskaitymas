from marius_s_mod1_atsiskaitymas.crawler import crawl

def main():
    crawl(site='kaunodiena.lt', timeout=5, format='list')

if __name__ == "__main__":
    main()
