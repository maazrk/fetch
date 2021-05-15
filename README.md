# fetch
A command line program that can fetch web pages and saves them to disk for later retrieval and browsing.

It also supports downloading related assets of the webpage specified

# Installation
This is a python script, and requires python3 interpreter to be installed and some packages.
To install the required packages, make use of the requirements.txt file
Run the following command:

`pip3 install -r requirements.txt`


tqdm==4.60.0 # for progressbar
requests==2.25.1 # for making http requests
beautifulsoup4==4.9.3 # for scraping the data

# Project structure

fetch.py - It is the entry point of the program

util.scraping_utils.py - Contains all the functions related to web scraping, making network calls i.e. extracting info from webpage, compressing the scraped data, etc.

util.helpers.py - Contains some helper functions for outputting the data and for validation

# Usage
usage: python3 fetch.py [options] urls

Fetch specified webpages

positional arguments:
  urls             Space separated urls to save

optional arguments:
  -h, --help       show this help message and exit
  -m, --meta    Displays metadata while fetching.
  -c, --clone  Extracts all assets from the page and saves it as a zip file

Eg: python3 fetch.py -m -c https://google.com https://netflix.com

