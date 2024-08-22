from internetarchive import upload
from termcolor import colored, cprint
import sys
import os
import time
import re

# TIME BETWEEN UPLOADS (SECONDS)
waittime = 180
# ENABLE FOR TESTING
testmode = False

# Print header
print(colored("\n ======= Archive.org IPA uploader... by 9021007 ======= \n", attrs=['reverse']))
print(colored("iOS Obscura Discord - https://discord.gg/5vmn6wPTpn", 'green'))
print(colored("Github - https://github.com/9021007/IPAUploader", 'green'))
print(colored("Made by 9021007 - https://links.9021007.xyz", 'green'))
print("")

# Check to make sure files are passed in
if (len(sys.argv) == 1):
    print("No files added as command arguments.")
    exit()
else:
    print(colored("Files passed in:", attrs=['bold', 'underline']))
    for i in range(len(sys.argv)):
        if (i == 0):
            continue
        print(sys.argv[i])
    print("\n")

# Ask the user if the files are correct
if (input(colored("Press enter to continue...", 'yellow')) == ""):
    pass
else:
    print("Cancelled.")
    exit()

filelist = sys.argv[1:]

if not os.path.exists("uploaded"):
    os.makedirs("uploaded")

for file in filelist:
    cpfile = file.replace(" ", "\ ").replace("(", "\(").replace(")", "\)")
    #copy file to current directory
    os.system(f'cp {cpfile} .')

    newfile = file.split('/')[-1]
    name = newfile.replace('.ipa', '').replace('_', ' ').replace("decrypted","Decrypted")
    identifier = re.sub(r'[^a-zA-Z0-9-]', '', name.replace('.', '-').replace(' ', '-')).lower() + '-ipa'

    # file will get sorted properly automatically by archive.org later, this is where all software goes
    collection = 'open_source_software'

    if (testmode):
        identifier = identifier + "-testing123"
        collection = 'test_collection'

    print("Now uploading " + colored(name, attrs=['bold']))

    md = {'collection': collection, 'title': name, 'mediatype': 'software'}
    r = upload(identifier, files=[newfile], metadata=md, verbose=True)

    if (r[0].status_code == 200):
        print ("\033[A\033[A") # reset cursor to beginning of previous line, so success message overwrites previous line
        print(colored(("Upload successful! - https://archive.org/details/" + identifier).ljust(os.get_terminal_size().columns), "green"))
        os.system(f'mv {cpfile} uploaded/') # move file to "uploaded" folder
        if (file != filelist[-1]):
            print(colored(("Waiting " + str(waittime) + " seconds before uploading next file... \n"), "light_grey"))
            time.sleep(waittime)
    else:
        print(colored("Upload failed.", "red"))
        exit()
    