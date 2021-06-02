import zipfile
import os

ftz = 'tickets2021con.txt'
zname = 'tickets2021con.zip'

def sizeMB(b):
    return round((b / (1024 * 1024)), 2)

if __name__ == "__main__":
    with zipfile.ZipFile(ftz, 'w') as myzip:
        myzip.write(zname)
    a1 = sizeMB(os.stat('tickets2021con.txt').st_size)
    a2 = sizeMB(os.stat('tickets2021con.zip').st_size)
    print(f'Size of original file: {a1} MB')
    print(f'Size of zipped file: {a2} MB')
