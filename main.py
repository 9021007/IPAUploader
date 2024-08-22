from internetarchive import upload
from termcolor import colored, cprint
import sys
import os
import time
import re
from shutil import copyfile
from bs4 import BeautifulSoup

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

if os.path.exists("Payload"):
    print(colored("Payload folder already exists in current directory, please remove it and try again.", "red"))
    exit()

for file in filelist:
    cpfile = file
    #copy file to current directory
    os.system(f'cp "{cpfile}" .')


    newfile = file.split('/')[-1]
    os.system(f'mv "{newfile}" "{newfile.replace(" ", "_")}"')
    newfile = newfile.replace(" ", "_")
    cpfile = cpfile.replace(" ", "_")
    name = newfile.replace('.ipa', '').replace('_', ' ').replace("decrypted","Decrypted")
    identifier = re.sub(r'[^a-zA-Z0-9-]', '', name.replace('.', '-').replace(' ', '-')).lower() + '-ipa'

    # Extract iPA
    zipfile = newfile.replace(".ipa", ".zip")#.replace(" ", "\ ").replace("(", "\(").replace(")", "\)")
    copyfile(newfile, zipfile)
    os.system(f'unzip "{zipfile}" > /dev/null')

    # get only directory in Payload folder to find Info.plist
    infoplist = os.listdir("Payload")[0] + "/Info.plist"

    bundleid = ""
    iconfile = ""

    # get bundle id and icon file name from Info.plist
    with open(f"Payload/{infoplist}", "r") as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'xml')
        iconfile = soup.find("key", string="CFBundleIcons").find_next("array").find("string").text
        bundleid = soup.find("key", string="CFBundleIdentifier").find_next("string").text

    # find icon file in full inside Payload/*/, since iconfile is only beginning of file name
    iconfile = [f for f in os.listdir(f"Payload/{os.listdir('Payload')[0]}") if iconfile in f][0]

    # copy icon file to current directory
    if (os.path.exists(f'Payload/{os.listdir("Payload")[0]}/{iconfile}')):
        os.system(f'cp "Payload/{os.listdir("Payload")[0]}/{iconfile}" .')
    else:
        os.system(f'cp "Payload/{os.listdir("Payload")[0]}/{iconfile}*" .')
    os.system(f'rm -rf Payload')

    # Archive.org cannot read the icon pngs, so a specific thumbnail is needed
    os.system(f'sips -s format jpeg "{iconfile}" --out _itemimage.jpg')

    # file will get sorted properly automatically by archive.org later, this is where all software goes
    collection = 'open_source_software'

    if (testmode):
        identifier = identifier + "-testing123"
        collection = 'test_collection'
        name = name + " (TESTING)"

    print("Now uploading " + colored(name, attrs=['bold']))

    md = {'collection': collection, 'title': name, 'mediatype': 'software', 'description': ('Decrypted iOS iPA file for "' + name.replace(" Decrypted", "") + '", with bundle ID ' + bundleid + "."), "subject": ("ipa;decrypted ipa;ios;" + bundleid)}
    if (testmode):
        if (input("Test mode, enter to upload...") != ""):
            print("Cancelled.")
            exit()

    # add "iconfile" to array below to upload icon uncompressed, though Archive.org cannot read it.
    r = upload(identifier, files=[newfile, "_itemimage.jpg"], metadata=md, verbose=True)

    if (r[0].status_code == 200):
        print ("\033[A\033[A") # reset cursor to beginning of previous line, so success message overwrites previous line
        print(colored(("Upload successful! - https://archive.org/details/" + identifier).ljust(os.get_terminal_size().columns), "green"))

        with open("uploaded.txt", "a") as f:
            f.write("https://archive.org/details/" + identifier + "\n")
            f.close()

        os.system(f'mv "{cpfile}" uploaded/') # move file to "uploaded" folder
        os.system(f'rm "{zipfile}"')
        os.system(f'rm "{iconfile}"')
        os.system(f'rm "{newfile}"')
        os.system('rm _itemimage.jpg')

        if (file != filelist[-1]):
            print(colored(("Waiting " + str(waittime) + " seconds before uploading next file... \n"), "light_grey"))
            time.sleep(waittime)
    else:
        print(colored("Upload failed.", "red"))
        exit()
    