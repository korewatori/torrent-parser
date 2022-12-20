# torrent-parser
A very simple Python torrent parser that I hacked together in a few hours. At the moment there are only options for generating a file list but I plan to include more with it.

This script can generate a file list for a torrent, in order of either alphabetical, smallest file first or largest file first. It can also tell you information about the torrent file such as when it was created and how many files it has (not in a list).

Sizes of the files in the torrent are displayed in (bytes/KB/MB/GB/TB) in brackets next to the path of the file. This can also be disabled.

## Usage
### torrent_parser.py
```
usage: torrent_parser.py [-h] [-o OUTPUT] [-s] [-l] [-b] [--no-file-size] {files,info} torrent_file

positional arguments:
  {files,info}          The command to execute
  torrent_file          The path to the torrent file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The file to output the results to
  -s, --sort-by-smallest
                        Sort the file list by size (smallest first)
  -l, --sort-by-largest
                        Sort the file list by size (largest first)
  -b, --show-in-bytes   Show file sizes in bytes rather than in a human readable way
  --no-file-size        Do not show file sizes in the file list, show purely files
```

## Examples
Generating a file list for a torrent file sorted alphanumerically, outputting the list to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py files <torrent_file.torrent> -o file_list.txt
```
Generating a file list for a torrent file sorted by largest file first, outputting the list to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py files <torrent_file.torrent> -l -o file_list.txt
```
Generating a file list for a torrent file sorted by smallest file first, outputting the list to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py files <torrent_file.torrent> -s -o file_list.txt
```
Getting information about the torrent: list for a torrent, outputting the info to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py info <torrent_file.torrent> -o file_list.txt
```

Note: the above script requires Python 3.
