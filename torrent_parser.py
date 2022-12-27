import argparse
import bencodepy
import os
import datetime
import hashlib

def parse_torrent_file(torrent_file, sort_by_size=False, smallest_first=False, show_in_bytes=False, no_file_size=False, search=None, no_paths=False, min_size=0, max_size=float('inf'), file_extension=None):
    with open(torrent_file, "rb") as f:
        torrent_contents = f.read()

    decoded_torrent = bencodepy.decode(torrent_contents)

    # Get the list of files from the decoded torrent
    if b'files' in decoded_torrent[b'info']:
        if isinstance(decoded_torrent[b'info'][b'files'], list):
            file_list = decoded_torrent[b'info'][b'files']
        else:
            file_list = [decoded_torrent[b'info'][b'files']]
    else:
        # If the 'files' field is not present, then the torrent file only contains a single file
        file_list = [{b'path': [decoded_torrent[b'info'][b'name']], b'length': decoded_torrent[b'info'][b'length']}]

    # Extract the file names and sizes from the file list
    file_info = []
    for file in file_list:
        path_strings = [p.decode("utf-8") for p in file[b'path']]
        file_name = "/".join(path_strings)
        if no_paths:
            file_name = path_strings[-1]
        file_size = file[b'length']
        file_info.append((file_name, file_size))


    # Filter the list of files by search term, if provided
    if search:
        file_info = [f for f in file_info if search.lower() in f[0].lower()]

    if show_in_bytes:
        file_info = [(file_name, "{:,}".format(file_size)) for file_name, file_size in file_info]

    # Filter the file list by size if the min_size or max_size arguments are provided
    if min_size is not None:
        file_info = [(file_name, file_size) for file_name, file_size in file_info if file_size >= min_size]
    if max_size is not None:
        file_info = [(file_name, file_size) for file_name, file_size in file_info if file_size <= max_size]
    if file_extension is not None:
        file_extension = file_extension.lower()
    if file_extension is not None:
        file_info = [(file_name, file_size) for file_name, file_size in file_info if file_name.lower().endswith(file_extension)]
    # Return an empty list if there are no files within the specified size range
    if not file_info:
        print("No files within the specified size range or specified file extension")
        return []

    if sort_by_size:
        if smallest_first:
            file_info.sort(key=lambda x: x[1])
        else:
            file_info.sort(key=lambda x: x[1], reverse=True)
    else:
        file_info.sort(key=lambda x: x[0])
    if show_in_bytes:
        file_info = [(file_name, file_size) for file_name, file_size in file_info]
    elif no_file_size:
        file_info = [file_name for file_name, _ in file_info]
    else:
        file_info = [(file_name, format_size(file_size)) for file_name, file_size in file_info]

    return file_info

def format_size(size):
    size = float(size)
    if size < 1024:
        # If the size is less than 1024 bytes, return it in bytes
        return "{} bytes".format(size)
    elif size < 1048576:
        # If the size is less than 1048576 bytes (1 MB), return it in KB
        return "{:.2f} KB".format(size / 1024)
    elif size < 1073741824:
        # If the size is less than 1073741824 bytes (1 GB), return it in MB
        return "{:.2f} MB".format(size / 1048576)
    elif size < 1099511627776:
        # If the size is less than 1099511627776 bytes (1 TB), return it in GB
        return "{:.2f} GB".format(size / 1073741824)
    else:
        # If the size is larger than 1099511627776 (1 TB), return it in TB
        return "{:.2f} TB".format(size / 1099511627776)


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def display_torrent_info(torrent_file, output_file=None):
    with open(torrent_file, "rb") as f:
        torrent_contents = f.read()

    decoded_torrent = bencodepy.decode(torrent_contents)

      # Extract the torrent name and creation date
    if b'name' in decoded_torrent[b'info']:
        name = decoded_torrent[b'info'][b'name'].decode('utf-8')
    else:
        name = "Unknown"

    human_date = "Unknown"
    unix_timestamp_createdAt = 0 or "Unknown"
    if b'creation date' in decoded_torrent:
        unix_timestamp_createdAt = decoded_torrent[b'creation date']
        human_date = datetime.datetime.fromtimestamp(unix_timestamp_createdAt).strftime("%Y-%m-%d %H:%M:%S")
        
    # Extract the announce URLs from the torrent
    if b'announce-list' in decoded_torrent:
        announce_urls = [url.decode('utf-8') for url_list in decoded_torrent[b'announce-list'] for url in url_list]
    elif b'announce' in decoded_torrent:
        announce_urls = [decoded_torrent[b'announce'].decode('utf-8')]
    else:
        announce_urls = []
    
        
    is_private = b'private' in decoded_torrent[b'info'] and decoded_torrent[b'info'][b'private'] == 1
    file_info = parse_torrent_file(torrent_file)
    
    
    # Get the list of files from the decoded torrent
    if b'files' in decoded_torrent[b'info']:
        if isinstance(decoded_torrent[b'info'][b'files'], list):
            file_list = decoded_torrent[b'info'][b'files']
        else:
            file_list = [decoded_torrent[b'info'][b'files']]
    else:
        # If the 'files' field is not present, then the torrent file only contains a single file
        file_list = [{b'path': [decoded_torrent[b'info'][b'name']], b'length': decoded_torrent[b'info'][b'length']}]

    # Calculate the total size of all the files in the torrent
    total_size = 0
    for file in file_list:
        file_size = file[b'length']
        total_size += file_size
        
    # Extract the "created with" information from the decoded torrent
    if b'created by' in decoded_torrent:
        created_by = decoded_torrent[b'created by'].decode("utf-8")
    else:
        created_by = "Unknown"

   # Extract the number of pieces and piece size from the torrent
    if b'pieces' in decoded_torrent[b'info']:
        num_pieces = len(decoded_torrent[b'info'][b'pieces'])
        piece_size = decoded_torrent[b'info'][b'piece length']
    else:
        num_pieces = "N/A"
        piece_size = "N/A"

    # Extract the comment from the torrent
    comment = "None"
    if b'comment' in decoded_torrent:
        comment = decoded_torrent[b'comment'].decode('utf-8')
        
    encoding = "N/A"
    if b'encoding' in decoded_torrent:
        encoding = decoded_torrent[b'encoding'].decode('utf-8')
    
    # Get the file name of the torrent file
    torrent_file_name = os.path.basename(torrent_file)

    # Get the hash of the torrent
    info_hash = hashlib.sha1(bencodepy.encode(decoded_torrent[b'info'])).hexdigest()

    # Print or write the torrent info to the console or file
    total_size = sum(file[b'length'] for file in file_list)
    if output_file:
        output_file.write("- - - - - Details for '{}': - - - - -\n\n".format(torrent_file_name))
        output_file.write("Name: {}\n".format(name))
        output_file.write("Torrent creation date: {} (Unix timestamp: {})\n".format(human_date, format(unix_timestamp_createdAt)))
        output_file.write("Number of files: {}\n".format(len(file_list)))
        output_file.write("Total size: {}\n".format(format_size(total_size)))
        output_file.write("Torrent infohash: {}\n".format(info_hash))
        output_file.write("Created by: {}\n".format(created_by))
        output_file.write("Number of Pieces: {} (x {})\n".format(num_pieces, format_size(piece_size)))
        output_file.write("Encoding: {}\n".format(encoding))
        if announce_urls:
            output_file.write("\nAnnounce URL(s):\n")
            for url in announce_urls:
                output_file.write("{}\n".format(url))
        else:
                output_file.write("Announce URL(s): N/A\n")
        if comment:
            output_file.write("\nComment: {}\n".format(comment))
        else:
            output_file.write("\nComment: None\n")        
        output_file.write("\nPrivate: {}\n".format(is_private))
    else:
        print("\n- - - - - Details for {}: - - - - -\n".format(torrent_file_name))
        print("Name: {}".format(name))
        print("Torrent creation date: {} (Unix timestamp: {})".format(human_date, format(unix_timestamp_createdAt)))
        print("Number of files: {}".format(len(file_list)))
        print("Total size: {}".format(format_size(total_size)))
        print("Torrent infohash: {}".format(info_hash))
        print("Created by: {}".format(created_by))
        print("Number of Pieces: {} (x {})".format(num_pieces, format_size(piece_size)))
        print("Encoding: {}\n".format(encoding))
        if announce_urls:
            print("Announce URL(s):")
            for url in announce_urls:
                print("{}".format(url))
        else:
                print("Announce URL(s): N/A")
        if comment:
            print("\nComment: {}\n".format(comment))
        else:
            print("\nComment: None\n")
        print("Private: {}".format(is_private))

def parse_size(size_str):
    """Parses a size string in the format '10mb' or '2gb' and returns the size in bytes"""
    size_str = size_str.lower()
    if size_str.endswith("kb"):
        return float(size_str[:-2]) * 1024
    elif size_str.endswith("mb"):
        return float(size_str[:-2]) * 1024 * 1024
    elif size_str.endswith("gb"):
        return float(size_str[:-2]) * 1024 * 1024 * 1024
    elif size_str.endswith("tb"):
        return float(size_str[:-2]) * 1024 * 1024 * 1024 * 1024
    else:
        # Assume the size is in bytes if no units are specified
        return float(size_str[:-2])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["info", "files", "magnet"], help="The command to execute")
    parser.add_argument("torrent_file", help="The path to the torrent file")
    parser.add_argument("-cl", "--clear", action="store_true", help="Clear the console before running the command")
    parser.add_argument("-o", "--output", help="The file to output the results to")
    parser.add_argument("-s", "--sort-by-smallest", action="store_true", help="Sort the file list by size (smallest first)")
    parser.add_argument("-l", "--sort-by-largest", action="store_true", help="Sort the file list by size (largest first)")
    parser.add_argument("-b", "--show-in-bytes", action="store_true", help="Show file sizes in bytes")
    parser.add_argument("--no-file-size", action="store_true", help="Do not show file sizes in the file list")
    parser.add_argument('--no-paths', action='store_true', help='Do not print the file path, only the files (redundant when used on a torrent that has multiple folders with the same file name)')
    parser.add_argument("-q", "--search", help="search the list of files for a particular term")
    parser.add_argument("--min-size", type=parse_size, help="Only include files equal to or larger than the specified size")
    parser.add_argument("--max-size", type=parse_size, help="Only include files equal to or smaller than the specified size")
    parser.add_argument("--file-extension", help="Filters file list by a specified file extension")
    args = parser.parse_args()

def generate_magnet_link(torrent_file):
    with open(torrent_file, "rb") as f:
        torrent_contents = f.read()

    decoded_torrent = bencodepy.decode(torrent_contents)
    info_hash = hashlib.sha1(bencodepy.encode(decoded_torrent[b'info'])).hexdigest()
    magnet_link = f"magnet:?xt=urn:btih:{info_hash}"

    return magnet_link

if args.command == "files":
    if args.search:
        if args.file_extension:
            print("Search results within torrent for: '{}' with a file extension of '{}'".format(args.search, args.file_extension))
        else:
            print("Search results within torrent for: '{}'".format(args.search))
    if args.clear:
        clear_console()
    file_info = parse_torrent_file(args.torrent_file, sort_by_size=args.sort_by_smallest or args.sort_by_largest, smallest_first=args.sort_by_smallest, show_in_bytes=args.show_in_bytes, search=args.search, no_paths=args.no_paths, min_size=args.min_size, max_size=args.max_size, file_extension=args.file_extension)
    if args.output:
        with open(args.output, "w") as f:
            for file_name, file_size in file_info:
                if args.no_file_size:
                    f.write("{}\n".format(file_name))
                elif args.show_in_bytes:
                    f.write("{} ({} bytes)\n".format(file_name, file_size))
                else:
                    f.write("{} ({})\n".format(file_name, file_size))

    else:
        # If no output file is specified, print the list of files to the console
        for file_name, file_size in file_info:
            if args.no_file_size:
                print("{}".format(file_name))
            elif args.show_in_bytes:
                print("{} ({} bytes)".format(file_name, file_size))
            else:
                print("{} ({})".format(file_name, file_size))

elif args.command == "info":
    if args.clear:
        clear_console()
    if args.output:
        with open(args.output, "w") as f:
            display_torrent_info(args.torrent_file, output_file=f)
    else:
        display_torrent_info(args.torrent_file)

if args.command == "magnet":
    if args.clear:
        clear_console()
    magnet_link = generate_magnet_link(args.torrent_file)
    torrent_file_name = os.path.basename(args.torrent_file)
    print("Magnet link for " + torrent_file_name + ": \n" + magnet_link)