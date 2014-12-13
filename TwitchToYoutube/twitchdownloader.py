import requests
import sys
import json
import re
import os
import string
import argparse
 
BASE_URL = 'https://api.twitch.tv'
 
def download_file(url, local_filename, cur_part, num_parts):
    chunk_size = 1024
    cur_length = 0
 
    r = requests.head(url)
    file_size = int(r.headers['Content-Length']) / float(pow(1024, 2))
    if r.headers['Content-Type'] != 'video/x-flv':
        raise Exception("Incorrect Content-Type ({0}) for {1}".format(headers['Content-Type'], url))
 
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if not chunk: # filter out keep-alive new chunks
                continue
            f.write(chunk)
            f.flush()
            cur_length += chunk_size
            sys.stdout.write("\rDownloading {0}/{1}: {2:.2f}/{3:.2f}MB ({4:.1f}%)".format(cur_part, num_parts, cur_length / float(pow(1024, 2)), file_size, ((cur_length / float(pow(1024, 2))) / file_size) * 100))
 
    print('...complete!')
 
def download_broadcast(id_, chunk_num):
    """ Download all video parts for broadcast 'id_' """
 
    pattern = "{base}/api/videos/a{id_}"
    url = pattern.format(base=BASE_URL, id_=id_)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("API returned {0}".format(r.status_code))
 
    try:
        j = r.json()
    except ValueError as e:
        print("API did not return valid JSON: {}".format(e))
        print("{}".format(r.text))
        quit()
 
    savepath = "{id_}".format(id_=id_)
    try:
        os.makedirs(savepath)
    except OSError:
        if not os.path.isdir(savepath):
            raise
 
    print ("Found {0} parts for broadcast ID {1} on channel '{2}'".format(len(j['chunks']['live']), id_, j['channel']))

    video_url = j["chunks"]["live"][chunk_num]["url"]
    ext = os.path.splitext(video_url)[1]
    filename = "{0}/{1}_{2:0>2}{3}".format(savepath, id_, chunk_num, ext)
    download_file(video_url, filename, chunk_num+1, len(j['chunks']['live']))
 
    print("Finished downloading broadcast ID {0} on channel '{1}'".format(id_, j['channel']))
    
def getChunkNum(id_, TimeInSeconds):
 
    pattern = "{base}/api/videos/a{id_}"
    url = pattern.format(base=BASE_URL, id_=id_)
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("API returned {0}".format(r.status_code))
 
    try:
        j = r.json()
    except ValueError as e:
        print("API did not return valid JSON: {}".format(e))
        print("{}".format(r.text))
        quit()

    print ("Found {0} parts for broadcast ID {1} on channel '{2}'".format(len(j['chunks']['live']), id_, j['channel']))
    
    CLength = 0
    ChunkNum = -1
    for nr, chunk in enumerate(j['chunks']["live"]):
        ChunkNum = ChunkNum+1
        print("Test" + str(nr))
        CLength = CLength + chunk["length"]
        print(chunk["length"])
        if CLength > TimeInSeconds:
            lst = [int(nr), TimeInSeconds-(CLength-chunk["length"])]
            return lst