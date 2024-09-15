from internetarchive import upload
from termcolor import colored, cprint
import sys
import os
import time
import re
from shutil import copyfile
from bs4 import BeautifulSoup
from biplist import *

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
    os.system(f'unzip -o "{zipfile}" > /dev/null')
    # get only directory in Payload folder to find Info.plist
    infoplist = os.listdir("Payload")[0] + "/Info.plist"

    bundleid = ""
    iconfile = ""
    appname = ""
    version = ""

    # get bundle id and icon file name from Info.plist
    with open(f"Payload/{infoplist}", "r") as f:
        try:
            contents = f.read()
            soup = BeautifulSoup(contents, 'xml')
            bundleid = soup.find("key", string="CFBundleIdentifier").find_next("string").text
            iconfile = soup.find("key", string="CFBundleIcons").find_next("array").find("string").text
            appname = soup.find("key", string="CFBundleDusplayName").find_next("string").text
            version = soup.find("key", string="CFBundleVersion").find_next("string").text
        except:
            contents = readPlist(f"Payload/{infoplist}")
            bundleid = contents["CFBundleIdentifier"]
            appname = contents["CFBundleDisplayName"]
            version = contents["CFBundleVersion"]
            try:
                iconfile = contents["CFBundleIcons"]["CFBundlePrimaryIcon"]["CFBundleIconFiles"][0]
            except:
                try:
                    iconfile = contents["Icon files"][0]
                except:
                    try:
                        iconfile = contents["CFBundleIconFiles"][0]
                    except:
                        # check if Icon.png exists
                        if (os.path.exists(f"Payload/{os.listdir('Payload')[0]}/Icon@2x.png")):
                            iconfile = "Icon@2x.png"
                        elif (os.path.exists(f"Payload/{os.listdir('Payload')[0]}/Icon.png")):
                            iconfile = "Icon.png"
                        else:
                            raise Exception("Icon file not found in Info.plist")
                            
                

    # if name contains more than 2 periods, replace name with appname
    if (name.count(".") > 2):
        print("Looks like we failed to parse the name from the filename. Using the app display name in the Bundle ID instead")
        name = appname + " " + version + " Decrypted"

    # find icon file in full inside Payload/*/, since iconfile is only beginning of file name
    iconfile = [f for f in os.listdir(f"Payload/{os.listdir('Payload')[0]}") if iconfile in f][0]

    # copy icon file to current directory
    if (os.path.exists(f'Payload/{os.listdir("Payload")[0]}/{iconfile}')):
        os.system(f'cp "Payload/{os.listdir("Payload")[0]}/{iconfile}" . > /dev/null')
    else:
        os.system(f'cp "Payload/{os.listdir("Payload")[0]}/{iconfile}*" . > /dev/null')


    if (testmode):
        input("Test mode, holding Payload folder open. Enter to continue...")
    os.system(f'rm -rf Payload')

    
    # Archive.org cannot read the icon pngs, so a specific thumbnail is needed
    os.system(f'sips -s format jpeg "{iconfile}" --out _itemimage.jpg > /dev/null')

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

        os.system(f'mv "{file}" uploaded/ && rm "{zipfile}" && rm "{iconfile}" && rm "{newfile}" && rm _itemimage.jpg') # move file to "uploaded" folder

        if (file != filelist[-1]):
            print(colored(("Waiting " + str(waittime) + " seconds before uploading next file... \n"), "light_grey"))
            time.sleep(waittime)
    else:
        print(colored("Upload failed.", "red"))
        exit()
    