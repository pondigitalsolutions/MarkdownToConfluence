import requests
import json
from MarkdownToConfluence.utils import get_all_page_names_in_filesystem, get_page_name_from_path
import MarkdownToConfluence.confluence.confluence_utils as confluence_utils
import sys
import os
import base64
from requests.auth import HTTPBasicAuth
from MarkdownToConfluence.confluence.confluence_utils import get_all_pages_in_space
import MarkdownToConfluence.globals
import MarkdownToConfluence.confluence.confluence_utils as confluence_utils

BASE_URL = os.environ.get("INPUT_CONFLUENCE_URL")
FILES_PATH = os.environ.get("INPUT_FILESLOCATION")
SPACE_KEY = os.environ.get("INPUT_CONFLUENCE_SPACE_KEY")
AUTH_USERNAME = os.environ.get("INPUT_AUTH_USERNAME")
AUTH_API_TOKEN = os.environ.get("INPUT_AUTH_API_TOKEN")
if (BASE_URL is None or AUTH_USERNAME is None or AUTH_API_TOKEN is None or SPACE_KEY is None or FILES_PATH is None):
    print("Missing environment variables")
    sys.exit(1)
auth = HTTPBasicAuth(AUTH_USERNAME, AUTH_API_TOKEN)


def delete_page_from_file(filename: str):
    page_name = get_page_name_from_path(filename, FILES_PATH)
    if (confluence_utils.page_exists_in_space(page_name, SPACE_KEY)):
        page_id = confluence_utils.get_page_id(page_name, SPACE_KEY)
        return delete_page(page_id)


def delete_page(page_id: str, page_name=""):

    url = f"{BASE_URL}/wiki/rest/api/content/{page_id}"

    headers = {
        'User-Agent': 'python'
    }

    response = requests.request('DELETE', url, headers=headers, auth=auth)

    if (response.status_code == 204):
        print(f"Deleted {page_id} {page_name}")
    else:
        print(
            f"Error occured while attempting to delete page: {page_id}, status code: {response.status_code}")

    return response


"""
    deletes all pages on confluence, that are not part of the files system.
    the exclude arg takes a list of page names, that are not to be deleted, even if they dont exist in the filesystem
"""


def delete_non_existing_descendants(space_key: str, root: str, exclude=[]):

    # url = f"{BASE_URL}/wiki/rest/api/content?spaceKey={space_key}"

    # headers = {
    # 'User-Agent': 'python'
    # }

    # results = []
    # response = requests.request("GET", url, headers=headers, auth=auth)
    # response_json = json.loads(response.text)
    # if(response.status_code == 200):
    #     results.extend(response_json['results'])
    #     while("next" in response_json['_links']):
    #         url = BASE_URL + response_json["_links"]["next"]
    #         response = requests.request("GET", url, headers=headers, auth=auth)
    #         response_json = json.loads(response.text)
    #         results.extend(response_json['results'])

    MarkdownToConfluence.globals.init()
    settings = MarkdownToConfluence.globals.settings
    if (settings != None and 'parent_name' in settings.keys()):
        pages_in_space = confluence_utils.get_all_descendants(
            settings['parent_page'], space_key)
    else:
        pages_in_space = confluence_utils.get_all_pages_in_space(space_key)

    pages_in_filesystem = get_all_page_names_in_filesystem(root)


def delete_all_pages_in_space(space_key):
    MarkdownToConfluence.globals.init()
    settings = MarkdownToConfluence.globals.settings
    parent_page = ""
    if (settings != None):
        if ('parent_page' in settings.keys()):
            parent_page = settings['parent_page']
    if (parent_page == ""):
        pages = get_all_pages_in_space(space_key)
    else:
        pages = confluence_utils.get_all_descendants(parent_page, space_key)


if __name__ == "__main__":
    if (sys.argv[1] == '--all'):
        delete_all_pages_in_space(SPACE_KEY)
    elif (sys.argv[1] == '--clean'):
        delete_non_existing_descendants(SPACE_KEY, FILES_PATH)
    else:
        delete_page_from_file(sys.argv[1])
