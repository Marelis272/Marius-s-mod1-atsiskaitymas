Web Article Crawler
A Python-based crawler for extracting article titles and associated image URLs from specific news websites (https://www.lrytas.lt/ and https://kauno.diena.lt/). It can output the data either as a list or append it to a CSV file while avoiding duplicate entries.

Features:
Extracts article titles and image URLs.
Supports two websites: Lrytas and Kauno Diena.
Handles timeouts during crawling to prevent long waits.
Outputs data as a Python list or appends to a CSV file.
Avoids duplicate entries in the CSV file.
Can skip invalid or duplicate articles with appropriate logging.

Requirements:
Python 3.8+

Required libraries:
requests
lxml
csv
os