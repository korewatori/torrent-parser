import argparse
import bencodepy

def parse_torrent_file(torrent_file, sort_by_size=False, smallest_first=False):
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

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("torrent_file", help="the torrent file to parse")
    parser.add_argument("-o", "--output", help="output file for the list of files")
    parser.add_argument("-s", "--sort-by-smallest", action="store_true", help="sort the list by size with the smallest files first")
    parser.add_argument("-l", "--sort-by-largest", action="store_true", help="sort the list by size with the largest files first")
    args = parser.parse_args()

    file_info = parse_torrent_file(args.torrent_file, sort_by_size=args.sort_by_smallest or args.sort_by_largest, smallest_first=args.sort_by_smallest)

    if args.output:
        with open(args.output, "w") as f:
            for file_name, file_size in file_info:
                f.write("{} ({})\n".format(file_name, format_size(file_size)))
    else:
        # If no output file is specified, print the list of files to the console
        for file_name, file_size in file_info:
            print("{} ({})".format(file_name, format_size(file_size)))
