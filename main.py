import internetarchive as ia
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

if (sys.platform.startswith('win32')):
    print(colored("Windows is not supported. Please use a Mac.", "red"))
    exit()
elif (sys.platform.startswith('linux')):
    print(colored("Linux is not supported. You will need to modify this script to make it work. Good luck.", "yellow"))
    if (input("Continue? (y/n) ") != "y"):
        exit()

# THANK YOU ego-lay-atman-bay FOR https://github.com/9021007/IPAUploader/issues/1
if (not ia.get_session().access_key) or (not ia.get_session().secret_key):
    print("Please enter your Internet Archive login credentials")
    ia.configure()

# Check to make sure files are passed in
if (len(sys.argv) == 1):
    print("No files added as command arguments.")
    exit()
else:
    print(colored("Files passed in: (" + str(len(sys.argv) - 1) + ")", attrs=['bold', 'underline']))
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
            appname = soup.find("key", string="CFBundleDisplayName").find_next("string").text
            version = soup.find("key", string="CFBundleVersion").find_next("string").text
        except:
            try:
                contents = f.read()
                soup = BeautifulSoup(contents, 'xml')
                appname = soup.find("key", string="CFBundleDisplayName").find_next("string").text
                version = soup.find("key", string="CFBundleVersion").find_next("string").text
                bundleid = soup.find("key", string="CFBundleIdentifier").find_next("string").text
            except:
                try:
                    contents = readPlist(f"Payload/{infoplist}")
                    bundleid = contents["CFBundleIdentifier"]
                    appname = contents["CFBundleDisplayName"]
                    version = contents["CFBundleVersion"]
                except:
                    contents = readPlist(f"Payload/{infoplist}")
                    bundleid = contents["CFBundleIdentifier"]
                    appname = contents["CFBundleName"]
                    version = contents["CFBundleVersion"]
                    




    def isfile_casesensitive(path):
        if not os.path.isfile(path): return False   # THANK YOU https://stackoverflow.com/questions/17277566/check-os-path-isfilefilename-with-case-sensitive-in-python
        directory, filename = os.path.split(path)
        if directory == '': directory = '.'
        return filename in os.listdir(directory)
           
    # TODO this needs to be reordered in order of highest resolution to lowest
    peckingorder = ["FreeIcon76x76~ipad.png","FreeIcon76x76@2x~ipad.png","FreeIcon72x72~ipad.png","FreeIcon72x72@2x~ipad.png","FreeIcon60x60@2x.png","FreeIcon57x57@2x.png","FreeIcon57x57.png","FreeIcon50x50~ipad.png","FreeIcon50x50@2x~ipad.png","FreeIcon40x40~ipad.png","FreeIcon40x40@2x~ipad.png","FreeIcon40x40@2x.png","FreeIcon29x29~ipad.png","FreeIcon29x29@2x~ipad.png","FreeIcon29x29@2x.png","FreeIcon29x29.png", "FreeIcon76x76", "FreeIcon72x72", "FreeIcon60x60", "FreeIcon57x57", "FreeIcon50x50", "FreeIcon40x40", "FreeIcon29x29", "AppIcon29x29@2x~ipad.png", "AppIcon29x29~ipad.png", "AppIcon40x40@2x~ipad.png", "AppIcon40x40~ipad.png", "AppIcon50x50@2x~ipad.png", "AppIcon50x50~ipad.png", "AppIcon57x57.png", "AppIcon57x57@2x.png", "AppIcon60x60@2x.png", "AppIcon72x72@2x~ipad.png", "AppIcon72x72~ipad.png", "AppIcon76x76@2x~ipad.png", "AppIcon76x76~ipad.png", "Icon@2x.png", "Icon.png", "ico.png"]


    if (isfile_casesensitive("iTunesArtwork")):
        iconfile = "iTunesArtwork"
    else:
        for i in range(len(peckingorder)):
            if (isfile_casesensitive(f"Payload/{os.listdir('Payload')[0]}/{peckingorder[i]}")):
                iconfile = peckingorder[i]
                break
            elif (i == len(peckingorder) - 1):
                print("Icon file not found in Payload folder, trying Info.plist...")
                with open(f"Payload/{infoplist}", "r") as f:
                    try:
                        contents = f.read()
                        soup = BeautifulSoup(contents, 'xml')
                        iconfile = soup.find("key", string="CFBundleIconFile").find_next("string").text
                    except:
                        try:
                            contents = f.read()
                            soup = BeautifulSoup(contents, 'xml')
                            iconfile = soup.find("key", string="CFBundleIconFiles").find_next("array").find_next("string").text
                        except:
                            contents = readPlist(f"Payload/{infoplist}")
                            try:
                                iconfile = contents["CFBundleIconFile"]
                            except:
                                iconfile = contents["CFBundleIconFiles"][0]
    if (iconfile == ""):
        raise Exception("Icon file not found")

    # if name contains more than 2 periods (as happens when it's a bundle ID), replace name with appname
    if (name.count(".") > 2):
        print("Looks like we failed to parse the name from the filename. Using the app display name in the Bundle ID instead")
        name = appname + " " + version + " Decrypted"



    if (iconfile == "iTunesArtwork"):
        iconfile = [f for f in os.listdir() if iconfile in f][0]
    else:
        iconfile = [f for f in os.listdir(f"Payload/{os.listdir('Payload')[0]}") if iconfile in f][0]
        # copy icon file to current directory
        if (os.path.exists(f'Payload/{os.listdir("Payload")[0]}/{iconfile}')):
            os.system(f'cp "Payload/{os.listdir("Payload")[0]}/{iconfile}" . > /dev/null')
        else:
            os.system(f'cp "Payload/{os.listdir("Payload")[0]}/{iconfile}*" . > /dev/null')


    if (testmode):
        input("Test mode, holding Payload folder open. Enter to continue...")
    os.system(f'rm -rf Payload')



    
    # Archive.org cannot read the icon pngs, so a specific thumbnail is needed. The thumbnails are usually in some weird format.
    # They, in my experinece, must be converted on a mac. Linux people, this might give you a hard time.
    os.system(f'sips -s format jpeg "{iconfile}" --out _itemimage.jpg > /dev/null')

    # file will get sorted properly automatically by archive.org later, this is where all software goes, even though this software is not open source.
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

    # OPTIONAL: add "iconfile" to array below to upload icon uncompressed, though Archive.org cannot read it.
    r = ia.upload(identifier, files=[newfile, "_itemimage.jpg"], metadata=md, verbose=True)

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
    