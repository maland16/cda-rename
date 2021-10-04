from tkinter import filedialog
from tkinter import *
from os import listdir, rename, path
from os.path import isfile, join


def main():
    root = Tk()
    root.withdraw()
    source_folder = filedialog.askdirectory(title="Select folder with .xml CDA records")
    destination_folder = filedialog.askdirectory(title="Select destination folder")

    if(source_folder == destination_folder):
        exit("ERROR: Source and destination folder are the same. To avoid overwriting, this is prohibited")

    print("Source folder: "+str(source_folder))
    print("Destination folder: "+str(destination_folder))

    
    files = [f for f in listdir(source_folder) if isfile(join(source_folder, f))]

    for file in files:
        source_file_path = source_folder + "/" + file

        print("Opening "+ source_file_path)

        with open(source_file_path, 'r') as f:
            data = f.read()

        # There are 23 characters in the search term, so we offset this
        first_name_start = data.find("<patient><name><family>") + 23
        first_name_end = first_name_start + data[first_name_start:].find("</family><given>")

        last_name_start = first_name_end + 16
        last_name_end = last_name_start + data[last_name_start:].find("</given>")

        # print("First start "+ str(first_name_start))
        # print("First end "+ str(first_name_end))    
        # print("Last start "+ str(last_name_start))
        # print("Last end "+ str(last_name_end))

        print("First name: " + data[first_name_start:first_name_end] + " Last name: " + data[last_name_start:last_name_end])

        # Renames as "<last name>, <first name>.xml"
        new_file_name = data[first_name_start:first_name_end] + ", " + data[last_name_start:last_name_end] + ".xml"

        new_file_name = new_file_name.replace("/","-") # sanitize for slashes

        dest_file_path = destination_folder + "/" + new_file_name

        # If there is already a file with the same name written, find a new name
        if path.exists(dest_file_path):

            modifier = 1
            # Keep incremeting the "modifier" number until there isn't a matching file already written
            while path.exists(dest_file_path[:-4] + "-" + str(modifier) + dest_file_path[-4:]):
                modifier += 1
            
            dest_file_path = dest_file_path[:-4] + "-" + str(modifier) + dest_file_path[-4:]

        print("Writing " + dest_file_path)

        # Rename those files!
        rename(source_file_path, dest_file_path)
    

if __name__ == "__main__":
    main()