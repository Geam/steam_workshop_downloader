#!/usr/bin/python3

import sys,getopt
import os

import urllib.request, urllib.parse, urllib
from urllib.error import HTTPError, URLError
import json

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

def read_plugin (output_dir, plugins_id_list):
    data = const_data['file']
    data['itemcount'] = len(plugins_id_list)
    for idx, plugin_id in enumerate(plugins_id_list):
        data['publishedfileids[' + str(idx) + ']'] = plugin_id
    encode_data = urllib.parse.urlencode(data).encode('ascii')
    try:
        response = urllib.request.urlopen(const_urls['file'], encode_data)
    except HTTPError as e:
        print("The server can't fullfill the request")
        print(e.code)
    except URLError as e:
        print("Can't reach server")
        print(e.reason)
    else:
        json_response = json.loads(response.read().decode('utf8'))
        temp = json_response['response']['publishedfiledetails'][0];
        for plugin in json_response['response']['publishedfiledetails']:
            print("Downloading " + plugin['publishedfileid'])
            path = os.path.join(output_dir, temp['publishedfileid'] + ".vpk")
            urllib.request.urlretrieve(plugin['file_url'], path)

def read_collection (collections_id_list):
    data = const_data['collection']
    data['collectioncount'] = len(collections_id_list)
    for idx, collection_id in enumerate(collections_id_list):
        data['publishedfileids[' + str(idx) + ']'] = collection_id
    encode_data = urllib.parse.urlencode(data).encode('ascii')
    try:
        response = urllib.request.urlopen(const_urls['collection'], encode_data)
    except HTTPError as e:
        print("The server can't fullfill the request")
        print(e.code)
    except URLError as e:
        print("Can't reach server")
        print(e.reason)
    else:
        json_response = json.loads(response.read().decode('utf-8'))
        sub_collection = []
        plugins_id_list = []
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
            plugins_id_list += read_collection(sub_collection)
        return plugins_id_list

def main(argv):
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
    plugins_id_list = read_collection(collections_id_list)
    read_plugin(output_dir, plugins_id_list)

if __name__ == "__main__":
    main(sys.argv)
