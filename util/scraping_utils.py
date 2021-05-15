import shutil
import requests
from urllib.parse import urlparse, urljoin
import os
import tempfile

def get_response(url):
  # Returns a session object and the response for the URL specified
  session = requests.Session()
  response = session.get(url)
  return response, session


def get_urlparse_objects(urls):
  # Returns the urlparse objects for the urls specified
  urlparse_objects = []
  for url in urls:
    urlparse_objects.append(urlparse(url))
  return urlparse_objects


def find_and_save_assets(pagefolder, url, soup, session, tag2find='img', inner='src'):
  # fetches and saves the specified tags present in the webpage
  if not os.path.exists(pagefolder): # create only once
    os.mkdir(pagefolder)
  for res in soup.findAll(tag2find):   # images, css, etc..
    try:
      filename = os.path.basename(res[inner])
      fileurl = urljoin(url, res.get(inner))
      # rename to saved file path
      # res[inner] # may or may not exist 
      filepath = os.path.join(pagefolder, filename)
      res[inner] = os.path.join(os.path.basename(pagefolder), filename)
      if not os.path.isfile(filepath): # was not downloaded
        with open(filepath, 'wb') as file:
          filebin = session.get(fileurl)
          file.write(filebin.content)
    except Exception as exc:
      pass
      # occurred possibly because there is no src attribute on the element fetched, 
      # It could mean that the asset content is present in the webpage itself
      #tqdm.write("Exception while fetching asset: {res}".format(res=res))
  return soup


def clone_webpage(url, soup, session):
  """ Creates an archive that contains the webpage and the specified assets
      tempfile.gettempdir() is used to store files in the temp location. 
      The files are deleted once the archive is created.
  """
  temp_dir = tempfile.gettempdir()
  url_object = urlparse(url)
  file_name = '{uri.netloc}{uri.path}'.format(uri=url_object).strip('/').replace('/', '-')
  folder_dir = temp_dir + '/' + file_name
  if os.path.exists(folder_dir): # delete if exists, to remove old data
    shutil.rmtree(folder_dir)
  os.mkdir(folder_dir)
  assets_folder = folder_dir + '/' + 'assets'

  soup = find_and_save_assets(assets_folder, url, soup, session, 'img', inner='src')
  soup = find_and_save_assets(assets_folder, url, soup, session, 'link', inner='href')
  soup = find_and_save_assets(assets_folder, url, soup, session, 'script', inner='src')

  with open(folder_dir + '/' + 'index.html', 'w') as file:
    file.write(soup.prettify())
  shutil.make_archive(file_name, 'zip', folder_dir)

  # Delete from temp once done
  shutil.rmtree(folder_dir)