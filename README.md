# torrent-parser
A very simple Python torrent parser that I hacked together in a few hours. At the moment there are only options for generating a file list but I plan to include more with it.

This script can generate a file list for a torrent, in order of either alphabetical, smallest file first or largest file first. 
Sizes of the files in the torrent are displayed in (bytes/KB/MB/GB/TB) in brackets next to the path of the file 

## Usage
### torrent_parser.py
```
usage: torrent_parser.py [-h] [-o OUTPUT] [-s] [-l] torrent_file

positional arguments:
  torrent_file          the torrent file to parse

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file for the list of files
  -s, --sort-by-smallest
                        sort the list by size with the smallest files first
  -l, --sort-by-largest
                        sort the list by size with the largest files first
```

## Examples
Generating a file list for a torrent file sorted alphanumerically, outputting the list to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py <torrent_file.torrent> -o file_list.txt
```
Generating a file list for a torrent file sorted by largest file first, outputting the list to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py <torrent_file.torrent> -l -o file_list.txt
```
Generating a file list for a torrent file sorted by smallest file first, outputting the list to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py <torrent_file.torrent> -s -o file_list.txt
```

Note: the above script requires Python 3.
