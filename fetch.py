import argparse
from tqdm import tqdm
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


# imports from other files
from util.scraping_utils import get_response, get_urlparse_objects, clone_webpage
from util.helpers import output_metadata, log_error, validate_urls

def cmdline_args():
  # Creates the parser
  my_parser = argparse.ArgumentParser(
    prog='fetch',
    usage='%(prog)s [options] urls',
    allow_abbrev=False,
    description='Fetch specified webpages',
    epilog='Refer to the README.txt for additional details'
  )

  # Add the arguments
  my_parser.add_argument(
    '-m',
    '--meta',
    action='store_true',
    help='Displays metadata while fetching.'
  )

  my_parser.add_argument(
    '-c',
    '--clone',
    action='store_true',
    help='Extracts all assets from the page and saves it as a zip file'
  )

  my_parser.add_argument(
    'urls',
    metavar='urls',
    type=str,
    nargs='+',
    help='Space separated urls to save'
  )

  # Execute the parse_args() method
  args = my_parser.parse_args()
  return args



# Begin execution
args = cmdline_args()

# Initial custom validation
urlparse_objects = get_urlparse_objects(args.urls)
validate_urls(urlparse_objects, args.urls)


# Start processing
for url in tqdm(args.urls, position=0):
  is_success = False
  error_message = ''

  try:
    tqdm.write("Fetching: {url}".format(url=url))
    response, session = get_response(url)
    response.raise_for_status() # Raise HTTPError if not successful
    is_success = True
  except requests.exceptions.Timeout:
    # Maybe set up for a retry, or continue in a retry loop
    error_message = "Request Timeout"
  except requests.exceptions.TooManyRedirects:
    # Tell the user their URL was bad and try a different one
    error_message = "Too many redirects!"
  except requests.exceptions.HTTPError as err:
    # received an error status code from server
    error_message = str(err)
  except requests.exceptions.RequestException as e:
    # something wrong with the URL
    error_message = "Invalid URL"
  finally:
    if not is_success:
      log_error(url, error_message)
      continue

  soup = BeautifulSoup(response.text, features="lxml")
  if args.meta:
    output_metadata(response, soup)
  url_object = urlparse(response.url)
  file_name = '{uri.netloc}{uri.path}'.format(uri=url_object).strip('/').replace('/', '-')
  if args.clone:
    clone_webpage(response.url, soup, session)
    tqdm.write("Saved zip file as {file_name}.zip\n".format(file_name=file_name))
  else:
    with open(file_name + '.html', 'w') as file:
      file.write(soup.prettify())
      tqdm.write("Saved HTML file as {file_name}.html\n".format(file_name=file_name))
