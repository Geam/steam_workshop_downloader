#!/usr/bin/python3

import sys,getopt
import os

import urllib.request, urllib.parse, urllib
from urllib.error import HTTPError, URLError
import json
import time

def usage(cmd, exit):
    print ("usge: " + cmd + "[-o <output_dir>] [<collection_id]... <collection_id>")
    sys.exit(exit)

const_urls = {
        'file' : "http://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1",
        'collection' : "http://api.steampowered.com/ISteamRemoteStorage/GetCollectionDetails/v0001"
        }
const_data = {
        'file' : {'itemcount' : 0, 'publishedfileids[0]' : 0},
        'collection' : {'collectioncount' : 0, 'publishedfileids[0]' : 0}
        }

def download_plugins (output_dir, plugins):
    fail = []
    error = 0
    for plugin in plugins:
        if 'file_url' in plugin:
            try:
                print("Downloading " + plugin['publishedfileid'] + ".vpk")
                path = os.path.join(output_dir, plugin['publishedfileid'] + ".vpk")
                urllib.request.urlretrieve(plugin['file_url'], path)
                print("Downloading complete")
                error += 1
            except HTTPError as e:
                print("Server return " + str(e.code) + " error on " + plugin['publishedfileid'] + " plugin")
                fail.append(plugin)
    return error, fail

def get_plugins_info (plugins_id_list):
    json_response = []
    error = None
    data = const_data['file']
    data['itemcount'] = len(plugins_id_list)
    for idx, plugin_id in enumerate(plugins_id_list):
        data['publishedfileids[' + str(idx) + ']'] = plugin_id
    encode_data = urllib.parse.urlencode(data).encode('ascii')
    try:
        response = urllib.request.urlopen(const_urls['file'], encode_data)
    except HTTPError as e:
        print("Server return " + str(e.code) + " error")
        error = e
    except URLError as e:
        print("Can't reach server: " + e.reason)
        error = e
    else:
        json_response = json.loads(response.read().decode('utf8'))
        json_response = json_response['response']['publishedfiledetails']
    return error, json_response

def get_plugins_id_from_collections_list (collections_id_list):
    sub_collection = []
    plugins_id_list = []
    error = None
    data = const_data['collection']
    data['collectioncount'] = len(collections_id_list)
    for idx, collection_id in enumerate(collections_id_list):
        data['publishedfileids[' + str(idx) + ']'] = collection_id
    encode_data = urllib.parse.urlencode(data).encode('ascii')
    try:
        response = urllib.request.urlopen(const_urls['collection'], encode_data)
    except HTTPError as e:
        print("Server return " + str(e.code) + " error")
        error = e
    except URLError as e:
        print("Can't reach server: " + e.reason)
        error = e
    else:
        json_response = json.loads(response.read().decode('utf-8'))
        for collection in json_response['response']['collectiondetails']:
            if 'children' in collection:
                for item in collection['children']:
                    if item['filetype'] == 0:
                        plugins_id_list.append(item['publishedfileid'])
                    elif item['filetype'] == 2:
                        sub_collection.append(item['publishedfileid'])
                    else:
                        print("Unrecognised filetype: " + str(item['filetype']))
        if len(sub_collection) > 0:
            error, plugins_id_list_temp = get_plugins_id_from_collections_list(sub_collection)
            if error == None:
                plugins_id_list += plugins_id_list_temp
    return error, plugins_id_list

def main(argv):
    sleep = 15
    output_dir = os.getcwd()
    if len(argv) == 1:
        usage(argv[0], 0)
    try:
        opts, args = getopt.getopt(argv[1:],"ho:")
    except getopt.GetoptError:
        usge(argv[0], 2)
    for opt, arg in opts:
        if opt == 'h':
            usge(argv[0], 0)
        elif opt == '-o':
            output_dir = os.path.abspath(arg)
    if not os.path.exists(output_dir):
        print(output_dir + ": path doesn't exist\nEnd of program")
        sys.exit(1)
    collections_id_list = argv[len(opts) * 2 + 1:]
    error, plugins_id_list = get_plugins_id_from_collections_list(collections_id_list)
    if error == None:
        error, plugins_info = get_plugins_info(plugins_id_list)
    if error == None:
        while len(plugins_info) > 0:
            error, plugins_info = download_plugins(output_dir, plugins_info)
            if error > 0:
                print("Some download fail, retrying in " + str(sleep) + " seconds")
                time.sleep(sleep)

if __name__ == "__main__":
    main(sys.argv)
