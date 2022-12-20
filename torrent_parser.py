import argparse
import bencodepy
import os
import datetime

def parse_torrent_file(torrent_file, sort_by_size=False, smallest_first=False, show_in_bytes=False, no_file_size=False):
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
        file_size = file[b'length']
        file_info.append((file_name, file_size))

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

def display_torrent_info(torrent_file, output_file=None):
    with open(torrent_file, "rb") as f:
        torrent_contents = f.read()

    decoded_torrent = bencodepy.decode(torrent_contents)

      # Extract the torrent name and creation date
    if b'name' in decoded_torrent[b'info']:
        name = decoded_torrent[b'info'][b'name'].decode('utf-8')
    else:
        name = "Unknown"

    human_date = "Unknown"  # Set default value for human_date
    if b'creation date' in decoded_torrent:
        unix_timestamp_createdAt = decoded_torrent[b'creation date']
        human_date = datetime.datetime.fromtimestamp(unix_timestamp_createdAt).strftime('%Y-%m-%d %H:%M:%S')
        
     # Extract the announce URLs
    if b'announce' in decoded_torrent:
        announce_urls = decoded_torrent[b'announce']
        if isinstance(announce_urls, list):
            announce_urls = [url.decode('utf-8') for url in announce_urls]
        else:
            announce_urls = [announce_urls.decode('utf-8')]
    else:
        announce_urls = ["N/A"]    
    
        
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

    # Get the file name of the torrent file
    torrent_file_name = os.path.basename(torrent_file)

    # Print or write the torrent info to the console or file
    total_size = sum(file[b'length'] for file in file_list)
    if output_file:
        output_file.write("- - - - - Details for {}: - - - - -\n\n".format(torrent_file_name))
        output_file.write("Name: {}\n".format(name))
        output_file.write("Torrent creation date: {}\n".format(human_date))
       # output_file.write("UNIX timestamp: {}\n".format(unix_timestamp_createdAt))
        output_file.write("Number of files: {}\n".format(len(file_list)))
        output_file.write("Total file size of file(s) in torrent: {}\n".format(format_size(total_size)))
        output_file.write("\nAnnounce URL(s):\n")
        for url in announce_urls:
                output_file.write("{}\n".format(url))
        output_file.write("\nPrivate?: {}\n".format(is_private))
    else:
        print("\n- - - - - Details for {}: - - - - -\n".format(torrent_file_name))
        print("Name: {}".format(name))
        print("Torrent creation date: {}".format(human_date))
      #  print("UNIX timestamp: {}".format(unix_timestamp_createdAt))
        print("Number of files: {}".format(len(file_list)))
        print("Total file size of file(s) in torrent: {}".format(format_size(total_size)))
        print("\nAnnounce URL(s):")
        for url in announce_urls:
                print("{}\n".format(url))
        print("Private?: {}".format(is_private))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["files", "info"], help="The command to execute")
    parser.add_argument("torrent_file", help="The path to the torrent file")
    parser.add_argument("-o", "--output", help="The file to output the results to")
    parser.add_argument("-s", "--sort-by-smallest", action="store_true", help="Sort the file list by size (smallest first)")
    parser.add_argument("-l", "--sort-by-largest", action="store_true", help="Sort the file list by size (largest first)")
    parser.add_argument("-b", "--show-in-bytes", action="store_true", help="Show file sizes in bytes")
    parser.add_argument("--no-file-size", action="store_true", help="Do not show file sizes in the file list")
    args = parser.parse_args()


if args.command == "files":
    file_info = parse_torrent_file(args.torrent_file, sort_by_size=args.sort_by_smallest or args.sort_by_largest, smallest_first=args.sort_by_smallest, show_in_bytes=args.show_in_bytes)
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
    if args.output:
        with open(args.output, "w") as f:
            display_torrent_info(args.torrent_file, output_file=f)
    else:
        display_torrent_info(args.torrent_file)
