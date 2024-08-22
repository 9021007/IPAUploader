# IPAUploader
 
A python script for uploading iOS iPA files to Archive.org.

## Installation

1. Have python installed. Tested with 3.11, but it should work on other versions too.
2. Have a macOS device. If you're on linux, you're on your own.
3. Install the `ia` tool with `brew install internetarchive`.
4. Run `ia configure` and follow the instructions.
5. Run `python3.11 -m pip install -r requirements.txt`.
6. Done!

## Usage

`python3.11 main.py [files]`

Yes, it works in bulk. Throw as many as you want at it.

## A word of warning

You very much **can** get rate-limited by Archive.org. If you upload too many files too quickly, you will get rate-limited. I'm not responsible for any rate-limits you get. Use at your own risk.

I have added a timeout variable to the top of the file. Don't be stupid.

