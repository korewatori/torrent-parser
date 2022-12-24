# torrent_parser
A very simple Python torrent parser that I hacked together in a few hours. At the moment this only returns basic information about torrents and cannot properly encode/decode torrents or create them (yet).

This script can generate a file list for a torrent, in order of either alphabetical, smallest file first or largest file first. It can also tell you information about the torrent file such as when it was created and how many files it has (not in a list).

Sizes of the files in the torrent are displayed in (bytes/KB/MB/GB/TB) in brackets next to the path of the file. This can also be disabled.

## Usage
### torrent_parser.py
```
usage: torrent_parser.py [-h] [-cl] [-o OUTPUT] [-s] [-l] [-b] [--no-file-size] [--no-paths] [-q SEARCH]
                         [--min-size MIN_SIZE] [--max-size MAX_SIZE] [--file-extension FILE_EXTENSION]
                         {info,files,magnet} torrent_file

positional arguments:
  {info,files,magnet}   The command to execute
  torrent_file          The path to the torrent file

optional arguments:
  -h, --help            show this help message and exit
  -cl, --clear          Clear the console before running the command
  -o OUTPUT, --output OUTPUT
                        The file to output the results to
  -s, --sort-by-smallest
                        Sort the file list by size (smallest first)
  -l, --sort-by-largest
                        Sort the file list by size (largest first)
  -b, --show-in-bytes   Show file sizes in bytes
  --no-file-size        Do not show file sizes in the file list
  --no-paths            Do not print the file path, only the files (redundant when used on a torrent that has multiple
                        folders with the same file name)
  -q SEARCH, --search SEARCH
                        search the list of files for a particular term
  --min-size MIN_SIZE   Only include files equal to or larger than the specified size
  --max-size MAX_SIZE   Only include files equal to or smaller than the specified size
  --file-extension FILE_EXTENSION
                        Filters file list by a specified file extension
```

## Examples
Generating a file list for a torrent file sorted by largest file first, outputting the list to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py files <torrent_file.torrent> -l -o file_list.txt
```
Generating a file list for a torrent file sorted by smallest file first, outputting the list to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py files <torrent_file.torrent> -s -o file_list.txt
```
Getting information about the torrent, outputting the information to a txt file in the current directory called "file_list.txt":
```
torrent_parser.py info <torrent_file.torrent> -o file_list.txt
```
Generating a magnet link from the provided torrent file, outputting the link to the console:
```
torrent_parser.py magnet <torrent_file.torrent>
```

Note: the above script requires Python 3.
