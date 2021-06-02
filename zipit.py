import zipfile
import zlib
import os

ftz = 'tickets2021con.txt'
zname = 'tickets2021con.zip'

def makeZip():
    with zipfile.ZipFile(zname, 'w', zipfile.ZIP_DEFLATED) as myzip:
        myzip.write(ftz)

def sizeMB(b):
    return round((b / (1024 * 1024)), 2)

if __name__ == "__main__":
    makeZip()
    a1 = sizeMB(os.stat(ftz).st_size)
    a2 = sizeMB(os.stat(zname).st_size)
    print(f'Size of original file: {a1} MB')
    print(f'Size of zipped file: {a2} MB')
