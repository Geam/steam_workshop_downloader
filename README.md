# Steam Workshop Content Downloader
Little script for downloading plugins from steam workshop for server that do not
support natively the workshop like left4dead2 server.

## How to use
Download the script and run it with the collection(s) id as arg. Note that it
will also download the content of the linked collection.

## Usage
### Command
```bash
./workshop.py [-o <output_dir] [<collection_id>]... collection_id
```

### Add a collection
Run the script with as many collection_id as you want
```bash
./workshop.py <collection_1_id> <collection_2_id> ... <collection_n_id>
```

### Add only a plugin
No, you can't and I don't want to implement it. Create a collection, your
players will thank you if you have more than one plugin. If you only have one
plugin, one day you will use many so create a collection.

### Update plugins
Just run the script
```bash
./workshop.py
```
Note that each time the script is call, the plugins will be updated if needed.
If you already have the plugins download, the script will redownload everything
the first time.

### Remove collection
Edit the addons.lst file :
    - remove the collection_id you don't want anymore
    - don't bother removing the plugins from the file, this part is
        re-generated each time the script is run.
You still need to remove manually the plugin (.vpk) file.

## Save file
The save file name addons.lst is write in json and has the following form :
```json
{
    "collections": [
        "<collection_1_id>",
        "<collection_2_id>",
        ...
        "<collection_n_id>"
    ],
    "plugins": {
        "<plugin_1_id>": {
            "title": "Title of the plugin",
            "time_updated": <last_updated_time_unix_timestamp>
        },
        "<plugin_2_id>": {
            "title": "Title of the plugin",
            "time_updated": <last_updated_time_unix_timestamp>
        },
        ...
        "<plugin_n_id>": {
            "title": "Title of the plugin",
            "time_updated": <last_updated_time_unix_timestamp>
        }
    }
```
This file is generated the first time you run the script with the collection(s)
id.

## Example
### First run
```bash
./workshop.py -o /path/to/l4d2/addons/workshop 313949717
```

### Add new collection
```bash
./workshop.py -o /path/to/l4d2/addons/workshop 313949718
```
Will download all plugins from 313949717 and 313949718 collections

### Update all plugins
```bash
./workshop.py
```

# Tags
steam workshop plugin collection download
