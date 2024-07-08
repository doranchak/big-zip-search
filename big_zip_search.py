import zipfile
import argparse

def search_text_in_large_zip(zip_path, filename, search_text):
    search_text_bytes = search_text.encode()
    chunk_size = 1024 * 1024  # 1MB chunks

    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        if filename in zip_file.namelist():
            with zip_file.open(filename) as file:
                partial_line = b''
                while True:
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    lines = chunk.split(b'\n')
                    lines[0] = partial_line + lines[0]  # Combine with leftover from previous chunk
                    partial_line = lines.pop()  # Save last part as it may be incomplete
                    for line in lines:
                        if search_text_bytes in line:
                            print(line.decode().strip())
                if partial_line and search_text_bytes in partial_line:  # Check any remaining part
                    print(partial_line.decode().strip())
        else:
            print(f"{filename} not found in the zip archive.")

def main():
    parser = argparse.ArgumentParser(description='Search for text within a file inside a zip archive.')
    parser.add_argument('zip_path', help='Path to the zip file')
    parser.add_argument('filename', help='Name of the file within the zip archive to search')
    parser.add_argument('search_text', help='Text to search for within the file')

    args = parser.parse_args()

    search_text_in_large_zip(args.zip_path, args.filename, args.search_text)

if __name__ == '__main__':
    main()
