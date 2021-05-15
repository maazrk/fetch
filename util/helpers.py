from datetime import datetime
from tqdm import tqdm
import sys

def output_metadata(response, soup):
  # Outputs the metadata of the request in the console
  tqdm.write("site: " + response.url)
  tqdm.write("num_links: "  + str(len(soup.findAll('link'))))
  tqdm.write("images: " + str(len(soup.findAll('img'))))
  tqdm.write("last_fetch: " + datetime.utcnow().strftime("%a %b %d %Y %H:%M UTC") + "\n")

def log_error(url, error_message):
  # Outputs the metadata of the request in the console
  tqdm.write("Error encountered while fetching {url}, error_message: {error_message}\n".format(url=url, error_message=error_message))


def validate_urls(url_objects, urls):
  # Performs a basic validation for checking presence of netloc and scheme
  for idx, url_object in enumerate(url_objects):
    if '' in [url_object.netloc, url_object.scheme]:
      tqdm.write("Invalid URL: '{url}', Expected format: https://google.com".format(url=urls[idx]))
      sys.exit()


