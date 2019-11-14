#!/usr/bin/env python

import requests
import os
import shutil
from os import listdir
from os.path import isfile, join

print('Welcome to Panopto Downloader~\n')
url = input('URL of one of the .ts files (use your favourite browser\'s dev tool): ')
fname = input('Name of output file: ')

url_filename = url.split('/')[-1]
dirname = url.split('/')[-2]

url_head = url[:-len(url_filename)]
#https://s-cloudfront.cdn.ap.panopto.com/sessions/99ee09e9-83bc-4084-9106-aac0009c58c1/436d46e5-2b84-434e-833e-aac0009c58c5-664139a6-17a6-4503-8896-aaaa002a5e03.hls/1249200/00000.ts

maxnum = 10 ** len(url_filename)-3 #last 3 chars are '.ts'
try:
    for i in range(maxnum):
        print('#Downloading file: ' + str(i) + '/' + str(maxnum))
        url_full = url_head + (lambda f: f(f))(lambda f: lambda x: x if len(x) == 5 else f(f)('0' + x))(str(i)) + '.ts'
        local_filename = '/'.join(url_full.split('/')[-2:])
        if not os.path.exists(dirname):
            os.makedirs(url_head.split('/')[-2])
        with requests.get(url_full, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)
except:
    pass

ts_filenames = [f for f in listdir(dirname) if isfile(join(dirname, f))]
ts_filenames.sort()
maxnum = len(ts_filenames)
with open(fname, 'wb') as merged:
	i = 0
	for ts_file in ts_filenames:
		print('#Converting file: ' + str(int(i/maxnum*100)) + '%')
		i += 1
		with open(dirname + '/' + ts_file, 'rb') as mergefile:
			shutil.copyfileobj(mergefile, merged)

shutil.rmtree(dirname)
