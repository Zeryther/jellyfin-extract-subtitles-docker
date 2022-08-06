#!/usr/bin/env python3
# Based on https://github.com/EraYaN/jellyfin-stats
# pip3 install requests tqdm

import os

URL = os.getenv('URL')
API_KEY = os.getenv('API_KEY')

from re import sub
import requests
from tqdm import tqdm

# Your server information
server_url = URL

class JellyfinAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["x-mediabrowser-token"] = self.token
        return r

auth=JellyfinAuth(API_KEY)
sess=requests.session()

# More requests can be made with
users = sess.get(f'{server_url}/Users', auth=auth)

if not users:
    print("Could not get users, please key API key and URL")
    exit()

user_id = ""

for user in users.json():
    if user['Policy']['IsAdministrator']:
        user_id = user['Id']
        print(f"Using administrator account {user['Name']} with id {user['Id']}")
        break

all_items = []

for itemtype in ["Episode", "Movie"]:
    start_index = 0
    limit = 1000
    items = []
    
    response = sess.get(f'{server_url}/Users/{user_id}/Items?IncludeItemTypes={itemtype}&Recursive=True&startIndex={start_index}&limit=0', auth=auth)
    if response:
        payload = response.json()
        total = payload['TotalRecordCount']
        if total > 0:
            pbar = tqdm(total=total, desc=f"Loading {itemtype}", unit='items', unit_scale=True, leave=True, dynamic_ncols=True)
            pbar.update(0)
            while total > start_index:
                response = sess.get(f'{server_url}/Users/{user_id}/Items?IncludeItemTypes={itemtype}&Recursive=True&Fields=MediaStreams,Path&startIndex={start_index}&limit={limit}&enableTotalRecordCount=false', auth=auth)
                if response:
                    payload = response.json()
                    items.extend(payload['Items'])
                    start_index += limit
                    pbar.update(len(payload['Items']))
                else:
                    break

            pbar.close()
    
    
    if len(items) > 0:
        all_items.extend(items)

subtitles = []
for item in all_items:
    path = item.get("Path")
    item_id = item["Id"]

    for stream in item.get("MediaStreams", []):
        if not stream.get("IsTextSubtitleStream") or stream.get("IsExternal") or not stream.get("SupportsExternalStream"):
            continue

        index = stream["Index"]
        codec = stream["Codec"]

        subtitles.append(f"{URL}/Videos/{item_id}/{item_id}/Subtitles/{index}/0/Stream.{codec}")

pbar = tqdm(total=len(subtitles), desc=f"Extracting subtitles", unit='items', unit_scale=True, leave=True, dynamic_ncols=True)
for i, url in enumerate(subtitles):
    pbar.update(1)
    res = sess.get(url, auth=auth, stream=True)
    res.close()

pbar.close()